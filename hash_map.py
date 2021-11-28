# Name: Allison Land
# OSU Email: landal@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7 - Hash Maps
# Due Date: 12/3/21
# Description: An implementation of a hash map using a dynamic array and chaining
#           using singly linked lists.


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the HashMap. Capacity of DynamicArray does not change.
        :param: None
        :return: None
        """
        self.size = 0
        for i in range(self.capacity):
            self.buckets[i] = LinkedList()

    def get(self, key: str) -> object:
        """
        Returns value associated with a given key. If key not in HashMap, returns None.
        :param: key (type:string)
        :return: value
        """
        index = self.hash_function(key)
        while index > self.capacity - 1:
            index = index % self.capacity
        LL = self.buckets[index]
        for node in LL:
                if node.key == key:
                    return node.value
        else:
            return None


    def put(self, key: str, value: object) -> None:
        """
        Places a key/value pair in the HashMap. If key already exists, then value is updated.
        :param: key (type:string), value (type:any)
        :return: None
        """
        index = self.hash_function(key)
        while index > self.capacity - 1:
            index = index % self.capacity
        if self.contains_key(key):          # update existing key
            LL = self.buckets[index]
            for node in LL:
                if node.key == key:
                    node.value = value
        else:                               # else add new key
            self.buckets[index].insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        If the given key exists in the HashMap, the key and associated value are removed.
        :param: key (type:string)
        :return: None
        """
        index = self.hash_function(key)
        while index > self.capacity - 1:
            index = index % self.capacity
        contains = self.contains_key(key)       # if key exists, then remove it
        if contains:
            self.buckets[index].remove(key)
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if specified key is present in the HashMap, else returns False.
        :param: key (type:string)
        :return: True or False (type:boolean)
        """
        index = self.hash_function(key)
        while index > self.capacity - 1:
            index = index % self.capacity
        LL = self.buckets[index].contains(key)
        if LL is not None:
            return True
        return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets (indices of the DynamicArray)
        which have no key/value pairs.
        :param: None
        :returns: number of empty buckets (type:integer)
        """
        empty = 0
        for i in range(self.capacity):
            if self.buckets[i].length() == 0:
                empty += 1
        return empty

    def table_load(self) -> float:
        """
        Returns the table load of the HashMap
        :param: None
        :returns: table load (type:integer)
        """
        table_load = self.size/self.capacity
        return table_load

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table based on the specified capacity. Rehashes the key/value pairs accordingly.
        :param: new capacity (type:integer)
        :return: None
        """
        if new_capacity < 1 or new_capacity == self.capacity:   # resize not necessary
            return
        else:
            old_capacity = self.capacity
            size = self.size
            if new_capacity > old_capacity:                     # if table is expanding
                self.capacity = new_capacity
                self.size = size
                for i in range(old_capacity, new_capacity):     # create more buckets in DynamicArray
                    self.buckets.append(LinkedList())
                for i in range(old_capacity):                   # rehash existing values based on new capacity
                    LL = self.buckets[i]
                    for node in LL:
                        if node is not None:
                            key = node.key
                            value = node.value
                            index = self.hash_function(key)
                            while index > new_capacity - 1:
                                index = index % new_capacity
                            if index != i:                      # if new index is same as old index, no move necessary
                                self.buckets[i].remove(key)     # else move key/value pair to new bucket
                                self.buckets[index].insert(key, value)

            else:                                               # if table is shrinking
                self.capacity = new_capacity
                for i in range(old_capacity):                   # rehash existing values
                    LL = self.buckets[i]
                    for node in LL:
                        if node is not None:
                            key = node.key
                            value = node.value
                            if new_capacity == 1:
                                self.buckets[0].insert(key, value)
                                self.buckets[i].remove(key)
                            else:
                                index = self.hash_function(key)
                                while index > new_capacity - 1:
                                    index = index % new_capacity
                                if index != i:                  # if new index is same as old index, no move necessary
                                    self.buckets[i].remove(key) # else move key/value pair to new bucket
                                    self.buckets[index].insert(key, value)

                for i in range(old_capacity, new_capacity, -1):     # remove excess buckets
                    self.buckets.pop()

    def get_keys(self) -> DynamicArray:
        """
        Returns all keys contained in the HashMap.
        :param: None
        :return: keys (type:DynamicArray)
        """
        da = DynamicArray()
        for i in range(self.capacity):
            LL = self.buckets[i]
            for node in LL:
                if node.key is not None:
                    da.append(node.key)
        return da


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
