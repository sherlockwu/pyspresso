#!/usr/bin/python
## @file        events.py
#  @brief       JDWP events.
#  @author      Jason Geffner
#  @copyright   CrowdStrike, Inc. 2016

from pyspresso.constants import EventKind


#
# Some docstrings in this module are copied directly from
# http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_Event_Composite
#

class Event:
    """ A JDWP event. For details, see
    http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_Event_Composite
    """

    event_kind = None
    """ An :any:`EventKind` value. """

    request_id = 0
    """ The ID of the request that generated this event. """


class VMStart(Event):
    """ Notification of initialization of a target VM. This event is received
    before the main thread is started and before any application code has been
    executed. Before this event occurs a significant amount of system code has
    executed and a number of system classes have been loaded. This event is
    always generated by the target VM, even if not explicitly requested.
    """

    event_kind = EventKind.VM_START

    thread = 0
    """ Initial thread. """

    _unpack_order = ("request_id", "thread")


class SingleStep(Event):
    """ Notification of step completion in the target VM. The step event is
    generated before the code at its location is executed. 
    """

    event_kind = EventKind.SINGLE_STEP

    thread = 0
    """ Stepped thread. """

    location = None
    """ Location stepped to. """

    _unpack_order = ("request_id", "thread", "location")

class Breakpoint(Event):
    """ Notification of a breakpoint in the target VM. The breakpoint event is
    generated before the code at its location is executed.
    """

    event_kind = EventKind.BREAKPOINT

    thread = 0
    """ Thread which hit breakpoint. """

    location = None
    """ Location hit. """

    _unpack_order = ("request_id", "thread", "location")

class MethodEntry(Event):
    """ Notification of a method invocation in the target VM. This event is
    generated before any code in the invoked method has executed. Method entry
    events are generated for both native and non-native methods.

    In some VMs method entry events can occur for a particular thread before
    its thread start event occurs if methods are called as part of the thread's
    initialization.
    """

    event_kind = EventKind.METHOD_ENTRY

    thread = 0
    """ Thread which entered method. """

    location = None
    """ The initial executable location in the method. """

    _unpack_order = ("request_id", "thread", "location")

class MethodExit(Event):
    """ Notification of a method return in the target VM. This event is
    generated after all code in the method has executed, but the location of
    this event is the last executed location in the method. Method exit events
    are generated for both native and non-native methods. Method exit events
    are not generated if the method terminates with a thrown exception.
    """

    event_kind = EventKind.METHOD_EXIT

    thread = 0
    """ Thread which exited method . """

    location = None
    """ Location of exit. """

    _unpack_order = ("request_id", "thread", "location")

class MethodExitWithReturnValue(Event):
    """ Notification of a method return in the target VM. This event is
    generated after all code in the method has executed, but the location of
    this event is the last executed location in the method. Method exit events
    are generated for both native and non-native methods. Method exit events
    are not generated if the method terminates with a thrown exception.
    """

    event_kind = EventKind.METHOD_EXIT_WITH_RETURN_VALUE

    thread = 0
    """ Thread which exited method. """

    location = None
    """ Location of exit. """

    value = None
    """ Value that will be returned by the method. """

    _unpack_order = ("request_id", "thread", "location", "value")

class MonitorContendedEnter(Event):
    """ Notification that a thread in the target VM is attempting to enter a
    monitor that is already acquired by another thread. Requires
    canRequestMonitorEvents capability - see
    http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_VirtualMachine_CapabilitiesNew.
    """

    event_kind = EventKind.MONITOR_CONTENDED_ENTER

    thread = 0
    """ Thread which is trying to enter the monitor. """

    object = None
    """ Monitor object reference. """

    location = None
    """ Location of contended monitor enter. """

    _unpack_order = ("request_id", "thread", "object", "location")

class MonitorContendedEntered(Event):
    """ Notification of a thread in the target VM is entering a monitor after
    waiting for it to be released by another thread. Requires
    canRequestMonitorEvents capability - see
    http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_VirtualMachine_CapabilitiesNew.
    """

    event_kind = EventKind.MONITOR_CONTENDED_ENTERED

    thread = 0
    """ Thread which entered monitor. """

    object = None
    """ Monitor object reference. """

    location = None
    """ Location of contended monitor enter. """

    _unpack_order = ("request_id", "thread", "object", "location")

class MonitorWait(Event):
    """ Notification of a thread about to wait on a monitor object. Requires
    canRequestMonitorEvents capability - see
    http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_VirtualMachine_CapabilitiesNew.
    """

    event_kind = EventKind.MONITOR_WAIT

    thread = 0
    """ Thread which is about to wait. """

    object = None
    """ Monitor object reference. """

    location = None
    """ Location at which the wait will occur. """

    timeout = 0
    """ Thread wait time in milliseconds. """

    _unpack_order = ("request_id", "thread", "object", "location", "timeout")

class MonitorWaited(Event):
    """ Notification that a thread in the target VM has finished waiting on
    Requires canRequestMonitorEvents capability - see
    http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_VirtualMachine_CapabilitiesNew.
    """

    event_kind = EventKind.MONITOR_WAITED

    thread = 0
    """ Thread which waited. """

    object = None
    """ Monitor object reference. """

    location = None
    """ Location at which the wait occured. """

    timed_out = False
    """ True if timed out. """

    _unpack_order = ("request_id", "thread", "object", "location", "timed_out")

class Exception(Event):
    """ Notification of an exception in the target VM. If the exception is
    thrown from a non-native method, the exception event is generated at the
    location where the exception is thrown. If the exception is thrown from a
    native method, the exception event is generated at the first non-native
    location reached after the exception is thrown.
    """

    event_kind = EventKind.EXCEPTION

    thread = 0
    """ Thread with exception. """

    location = None
    """ Location of exception throw (or first non-native location after throw
    if thrown from a native method).
    """

    exception = 0
    """ Thrown exception. """

    catch_location = None
    """ Location of catch, or 0 if not caught. An exception is considered to be
    caught if, at the point of the throw, the current location is dynamically
    enclosed in a try statement that handles the exception. (See the JVM
    specification for details). If there is such a try statement, the catch
    location is the first location in the appropriate catch clause.

    If there are native methods in the call stack at the time of the exception,
    there are important restrictions to note about the returned catch location.
    In such cases, it is not possible to predict whether an exception will be
    handled by some native method on the call stack. Thus, it is possible that
    exceptions considered uncaught here will, in fact, be handled by a native
    method and not cause termination of the target VM. Furthermore, it cannot
    be assumed that the catch location returned here will ever be reached by
    the throwing thread. If there is a native frame between the current
    location and the catch location, the exception might be handled and cleared
    in that native method instead.

    Note that compilers can generate try-catch blocks in some cases where they
    are not explicit in the source code; for example, the code generated for
    synchronized and finally blocks can contain implicit try-catch blocks. If
    such an implicitly generated try-catch is present on the call stack at the
    time of the throw, the exception will be considered caught even though it
    appears to be uncaught from examination of the source code.
    """

    _unpack_order = ("request_id", "thread", "location", "exception",
                     "catch_location")

class ThreadStart(Event):
    """ Notification of a new running thread in the target VM. The new thread
    can be the result of a call to java.lang.Thread.start or the result of
    attaching a new thread to the VM though JNI. The notification is generated
    by the new thread some time before its execution starts. Because of this
    timing, it is possible to receive other events for the thread before this
    event is received. (Notably, Method Entry Events and Method Exit Events
    might occur during thread initialization. It is also possible for the
    VirtualMachine AllThreads command
    (http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_VirtualMachine_AllThreads)
    to return a thread before its thread start event is received.

    Note that this event gives no information about the creation of the thread
    object which may have happened much earlier, depending on the VM being
    debugged.
    """

    event_kind = EventKind.THREAD_START
    
    thread = 0
    """ Started thread. """

    _unpack_order = ("request_id", "thread")

class ThreadDeath(Event):
    """ Notification of a completed thread in the target VM. The notification
    is generated by the dying thread before it terminates. Because of this
    timing, it is possible for {@link VirtualMachine#allThreads} to return this
    thread after this event is received.

    Note that this event gives no information about the lifetime of the thread
    object. It may or may not be collected soon depending on what references
    exist in the target VM.
    """

    event_kind = EventKind.THREAD_DEATH

    thread = 0
    """ Ending thread. """

    _unpack_order = ("request_id", "thread")

class ClassPrepare(Event):
    """ Notification of a class prepare in the target VM. See the JVM
    specification for a definition of class preparation. Class prepare events
    are not generated for primtiive classes (for example,
    java.lang.Integer.TYPE).
    """

    event_kind = EventKind.CLASS_PREPARE

    thread = 0
    """ Preparing thread. In rare cases, this event may occur in a debugger
    system thread within the target VM. Debugger threads take precautions to
    prevent these events, but they cannot be avoided under some conditions,
    especially for some subclasses of java.lang.Error. If the event was
    generated by a debugger system thread, the value returned by this method is
    null, and if the requested suspend policy
    (http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_SuspendPolicy)
    for the event was EVENT_THREAD all threads will be suspended instead, and
    the composite event's suspend policy will reflect this change.

    Note that the discussion above does not apply to system threads created by
    the target VM during its normal (non-debug) operation.
    """

    ref_type_tag = 0
    """ Kind of reference type. See JDWP.TypeTag
    (http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_TypeTag).
    """

    type_id = 0
    """ Type being prepared. """

    signature = ""
    """ Type signature. """

    status = 0
    """ Status of type. See JDWP.ClassStatus
    (http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_ClassStatus).
    """

    _unpack_order = ("request_id", "thread", "ref_type_tag", "type_id",
                     "signature", "status")

class ClassUnload(Event):
    """ Notification of a class unload in the target VM.

    There are severe constraints on the debugger back-end during garbage
    collection, so unload information is greatly limited.
    """

    event_kind = EventKind.CLASS_UNLOAD

    signature = ""
    """ Type signature. """

    _unpack_order = ("request_id", "signature")

class FieldAccess(Event):
    """ Notification of a field access in the target VM. Field modifications
    are not considered field accesses. Requires canWatchFieldAccess capability
    - see
    http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_VirtualMachine_CapabilitiesNew.
    """

    event_kind = EventKind.FIELD_ACCESS

    thread = 0
    """ Accessing thread. """

    location = None
    """ Location of access. """

    ref_type_tag = 0
    """ Kind of reference type. See JDWP.TypeTag
    (http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_TypeTag).
    """

    type_id = 0
    """ Type of field. """

    field_id = 0
    """ Field being accessed. """

    object = None
    """ Object being accessed (null for statics). """

    _unpack_order = ("request_id", "thread", "location", "ref_type_tag",
                     "type_id", "field_id", "object")

class FieldModification(Event):
    """ Notification of a field modification in the target VM. Requires
    canWatchFieldModification capability - see
    http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_VirtualMachine_CapabilitiesNew.
    """

    event_kind = EventKind.FIELD_MODIFICATION

    thread = 0
    """ Modifying thread. """

    location = None
    """ Location of modify. """

    ref_type_tag = 0
    """ Kind of reference type. See JDWP.TypeTag
    (http://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html#JDWP_TypeTag).
    """

    type_id = 0
    """ Type of field. """

    field_id = 0
    """ Field being modified. """

    object = None
    """ Object being accessed (null for statics). """

    value_to_be = None
    """ Value to be assigned. """

    _unpack_order = ("request_id", "thread", "location", "ref_type_tag",
                     "type_id", "field_id", "object", "value_to_be")

class VMDeath(Event):
    event_kind = EventKind.VM_DEATH

    _unpack_order = ("request_id",)