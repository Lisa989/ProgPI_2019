class MyQueueUndoRedo:
    """
    Coda di redo e undo
    """
    N_MAX = 10

    def __init__(self, parent):
        self.parent = parent
        self.__queue_redo = []
        self.__queue_undo = []

    def take_undo(self):
        n = len(self.__queue_undo)
        if n == 0:
            return None
        el = self.__queue_undo.pop(n - 1)
        self.__put_redo(el)
        if self.is_queue_undo_empty():
            self.parent.enable_undo(False)
        return el

    def __put_redo(self, el):
        if self.is_queue_redo_empty():
            self.parent.enable_redo(True)
        self.__queue_redo.append(el)
        if len(self.__queue_redo) >= MyQueueUndoRedo.N_MAX:
            self.__queue_redo.pop(0)

    def put_undo(self, el):
        if self.is_queue_undo_empty():
            self.parent.enable_undo(True)
        self.__queue_undo.append(el)
        if len(self.__queue_undo) > MyQueueUndoRedo.N_MAX:
            self.__queue_undo.pop(0)

    def take_redo(self):
        n = len(self.__queue_redo)
        if n == 0:
            return None
        el = self.__queue_redo.pop(n - 1)
        self.put_undo(el)
        if self.is_queue_redo_empty():
            self.parent.enable_redo(False)
        return el

    def is_queue_redo_empty(self):
        return len(self.__queue_redo) == 0

    def is_queue_undo_empty(self):
        return len(self.__queue_undo) == 0

    def clear_redo(self):
        self.__queue_redo.clear()
        if self.is_queue_redo_empty():
            self.parent.enable_redo(False)

    def clear_undo(self):
        self.__queue_undo.clear()
        if self.is_queue_undo_empty():
            self.parent.enable_undo(False)
