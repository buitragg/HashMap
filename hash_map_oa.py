# Name: Gian Buitrago
# OSU Email: buitragg@oregonstate.com
# Course: CS261 - Data Structures
# Assignment: Hash Table
# Due Date: March 17, 2023
# Description: Implementation of hash table with open addressing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method adds a key to the map using quadratic probing.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        index = self._hash_function(key) % self._capacity
        # if index is empty add key and value
        if self._buckets[index] is None:
            self._size += 1
            self._buckets[index] = HashEntry(key, value)
            self._buckets[index].is_tombstone = False
            return
        # if there is collision using quadratic probing
        else:
            counter = 0
            new_index = (index + counter ** 2) % self._capacity
            while self._buckets[new_index] is not None:
                # if there is a tombstone switch create a new hash entry
                if self._buckets[new_index].key == key:
                    self._buckets[new_index].value = value
                    self._buckets[new_index].is_tombstone = False

                    return
                elif self._buckets[new_index].is_tombstone:
                    self._buckets[new_index].is_tombstone = False
                    self._buckets[new_index] = value
                    self._size += 1

                    return
                # update counter for probing and new_index
                counter += 1
                new_index = (index + counter ** 2) % self._capacity
            # update size and add another hash entry to the new index
            self._size += 1
            self._buckets[new_index] = HashEntry(key, value)
            self._buckets[new_index].is_tombstone = False

    def table_load(self) -> float:
        """
        Return load factor
        """
        # load factor is size/capacity
        return self._size/self._capacity


    def empty_buckets(self) -> int:
        """
        Method will return empty buckets
        """
        # because we are in an array the difference between size and capacity will be the empty buckets
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Method for table resize
        """
        if new_capacity < 1 or self._size > new_capacity:
            return
            # if capacity is not a primer number make it the next prime, if it is a prime number make new capacity
        if self._is_prime(new_capacity) is False:
            prime_capacity = self._next_prime(new_capacity)
        else:
            prime_capacity = new_capacity

        old_capacity = self._capacity
        self._capacity = prime_capacity
        temp = self._buckets

        # this resize will work like the DA resizing. create a new array and append the old to the new with the new capacity
        new_arr = DynamicArray()
        for i in range(prime_capacity):
            new_arr.append(None)
        self._buckets = new_arr
        self._size = 0
        for i in range(old_capacity):
            i = temp[i]
            if i is not None:
                self.put(i.key, i.value)

    def get(self, key: str) -> object:
        """
        Get value of key from map o
        """
        # traverse array if key is four return value if not return None
        for i in range(self._buckets.length()):
            if self._buckets[i] is not None and self._buckets[i].key == key and not self._buckets[i].is_tombstone:
                return self._buckets[i].value
        # if not found return None
        return

    def contains_key(self, key: str) -> bool:
        """
        Method Return true if key is present, false otherwise
        """
        # traverse array if key is four return value if not return None
        for i in range(self._buckets.length()):
            if self._buckets[i] is not None and self._buckets[i].key == key:
                return True
        # if not found return None
        return False

    def remove(self, key: str) -> None:
        """
        Method will remove key and value if the key has no value the method does nothing
        """
        index = self._hash_function(key) % self._capacity
        arr_val = self._buckets[index]
        counter = 0
        if arr_val is None:
            return None

        else:
            while arr_val is not None:
                if arr_val.key == key and not arr_val.is_tombstone:
                    arr_val.is_tombstone = True
                    self._size -= 1
                    return None
                arr_val = self._buckets[(index + counter ** 2) % self._capacity]
                counter += 1

    def clear(self) -> None:
        """
        Method clears the map
        """
        for i in range(self._buckets.length()):
            self._buckets[i] = None
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method return array with keys and values
        """
        ##create new array
        new_arr = DynamicArray()
        # traverse hash and append values and keys to nre array. return new array
        for i in range(self._buckets.length()):
            if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                new_arr.append((self._buckets[i].key, self._buckets[i].value))
        return new_arr


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
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
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
