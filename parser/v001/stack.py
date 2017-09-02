#!/usr/bin/env python

class Stack():

    def __init__(self):
        self._store = []
        self.reset()

    def push(self, item):
        try:
            self._store.append(item)
        except Exception as xxx:
            print xxx

        self.cnt = self.cnt+1

    def pop(self):
        if len(self._store) == 0: return None
        item = self._store.pop(len(self.store) - 1) 
        return item

    def get(self):
        if len(self._store) == 0: return None
        item = self._store.pop(0)
        return item
    
    # Non destructive pop
    def pop2(self):
        if self.cnt <= 0: return None
        self.cnt = self.cnt - 1
        item = self._store[self.cnt] 
        return item

    # Non destructive get
    def get2(self):
        if self.gcnt >= len(self._store): return None
        item = self._store[self.gcnt] 
        self.gcnt = self.gcnt + 1
        return item
   
    # Start counters fresh 
    def reset(self):
        self.cnt = 0
        self.gcnt = 0

    def stacklen():
        return len(self._store)

