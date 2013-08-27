# -*- coding: utf-8 -*-

# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Copyright (C) 2012 Yahoo! Inc. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc
import threading

from billingstack.openstack.common import uuidutils

from billingstack.taskflow import exceptions as exc
from billingstack.taskflow import states
from billingstack.taskflow import utils


class Flow(object):
    """The base abstract class of all flow implementations.

    It provides a set of parents to flows that have a concept of parent flows
    as well as a state and state utility functions to the deriving classes. It
    also provides a name and an identifier (uuid or other) to the flow so that
    it can be uniquely identifed among many flows.

    Flows are expected to provide (if desired) the following methods:
    - add
    - add_many
    - interrupt
    - reset
    - rollback
    - run
    - soft_reset
    """

    __metaclass__ = abc.ABCMeta

    # Common states that certain actions can be performed in. If the flow
    # is not in these sets of states then it is likely that the flow operation
    # can not succeed.
    RESETTABLE_STATES = set([
        states.INTERRUPTED,
        states.SUCCESS,
        states.PENDING,
        states.FAILURE,
    ])
    SOFT_RESETTABLE_STATES = set([
        states.INTERRUPTED,
    ])
    UNINTERRUPTIBLE_STATES = set([
        states.FAILURE,
        states.SUCCESS,
        states.PENDING,
    ])
    RUNNABLE_STATES = set([
        states.PENDING,
    ])

    def __init__(self, name, parents=None, uuid=None):
        self._name = str(name)
        # The state of this flow.
        self._state = states.PENDING
        # If this flow has a parent flow/s which need to be reverted if
        # this flow fails then please include them here to allow this child
        # to call the parents...
        if parents:
            self.parents = tuple(parents)
        else:
            self.parents = tuple([])
        # Any objects that want to listen when a wf/task starts/stops/completes
        # or errors should be registered here. This can be used to monitor
        # progress and record tasks finishing (so that it becomes possible to
        # store the result of a task in some persistent or semi-persistent
        # storage backend).
        self.notifier = utils.TransitionNotifier()
        self.task_notifier = utils.TransitionNotifier()
        # Assign this flow a unique identifer.
        if uuid:
            self._id = str(uuid)
        else:
            self._id = uuidutils.generate_uuid()
        # Ensure we can not change the state at the same time in 2 different
        # threads.
        self._state_lock = threading.RLock()

    @property
    def name(self):
        """A non-unique name for this flow (human readable)"""
        return self._name

    @property
    def uuid(self):
        return self._id

    @property
    def state(self):
        """Provides a read-only view of the flow state."""
        return self._state

    def _change_state(self, context, new_state, check_func=None, notify=True):
        old_state = None
        changed = False
        with self._state_lock:
            if self.state != new_state:
                if (not check_func or
                   (check_func and check_func(self.state))):
                    changed = True
                    old_state = self.state
                    self._state = new_state
        # Don't notify while holding the lock so that the reciever of said
        # notifications can actually perform operations on the given flow
        # without getting into deadlock.
        if notify and changed:
            self.notifier.notify(self.state, details={
                'context': context,
                'flow': self,
                'old_state': old_state,
            })
        return changed

    def __str__(self):
        lines = ["Flow: %s" % (self.name)]
        lines.append("%s" % (self.uuid))
        lines.append("%s" % (len(self.parents)))
        lines.append("%s" % (self.state))
        return "; ".join(lines)

    @abc.abstractmethod
    def add(self, task):
        """Adds a given task to this flow.

        Returns the uuid that is associated with the task for later operations
        before and after it is ran.
        """
        raise NotImplementedError()

    def add_many(self, tasks):
        """Adds many tasks to this flow.

        Returns a list of uuids (one for each task added).
        """
        uuids = []
        for t in tasks:
            uuids.append(self.add(t))
        return uuids

    def interrupt(self):
        """Attempts to interrupt the current flow and any tasks that are
        currently not running in the flow.

        Returns how many tasks were interrupted (if any).
        """
        def check():
            if self.state in self.UNINTERRUPTIBLE_STATES:
                raise exc.InvalidStateException(("Can not interrupt when"
                                                 " in state %s") % self.state)

        check()
        with self._state_lock:
            check()
            self._change_state(None, states.INTERRUPTED)
            return 0

    def reset(self):
        """Fully resets the internal state of this flow, allowing for the flow
        to be ran again.

        Note: Listeners are also reset.
        """
        def check():
            if self.state not in self.RESETTABLE_STATES:
                raise exc.InvalidStateException(("Can not reset when"
                                                 " in state %s") % self.state)

        check()
        with self._state_lock:
            check()
            self.notifier.reset()
            self.task_notifier.reset()
            self._change_state(None, states.PENDING)

    def soft_reset(self):
        """Partially resets the internal state of this flow, allowing for the
        flow to be ran again from an interrupted state.
        """
        def check():
            if self.state not in self.SOFT_RESETTABLE_STATES:
                raise exc.InvalidStateException(("Can not soft reset when"
                                                 " in state %s") % self.state)

        check()
        with self._state_lock:
            check()
            self._change_state(None, states.PENDING)

    @abc.abstractmethod
    def run(self, context, *args, **kwargs):
        """Executes the workflow."""
        raise NotImplementedError()

    def rollback(self, context, cause):
        """Performs rollback of this workflow and any attached parent workflows
        if present.
        """
        pass
