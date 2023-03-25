# Name: Gian Buitrago
# OSU Email: buitragg@oregonstate.com
# Course: CS261 - Data Structures
# Assignment: Hash Table
# Due Date: March 17, 2023
# Description: Implementation of hash table


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Method to insert key-value pair into map
        """
        # if load factor is greater or equal to 1 double capacity
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)
        # Modulo to keep the index within the bounds of the array
        index = self._hash_function(key) % self._capacity
        node = self._buckets[index]
        # check if index is not empty
        if node.length() > 0:
            # if index is not empty check if index contains value
            old_value = node.contains(key)
            if old_value:
                # if contain switch values and make no changes
                old_value.value = value
            else:
                # else add value
                node.insert(key, value)
                self._size += 1
        # if the index is empty just add value
        else:
            node.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Return count of empty buckets
        """
        count = 0
        for index in range(self._capacity):
            # count all empty index in the capacity of the array
            if self._buckets[index].length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Method return table load
        """
        return self._size/self._capacity

    def clear(self) -> None:
        """
        Method clears the map
        """
        # create empty linked list
        empty_list = LinkedList()
        size = self._buckets.length()

        for i in range(size):
            # if index is not empty switch with empty list
            if self._buckets[i].length() != 0:
                self._buckets[i] = empty_list
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        """
        if new_capacity < 1:
            return
            # if capacity is not a primer number make it the next prime, if it is a prime number make new capacity
        if self._is_prime(new_capacity) is False:
            prime_capacity = self._next_prime(new_capacity)
        else:
            prime_capacity = new_capacity

        old_capacity = self._capacity
        self._capacity = prime_capacity

        # expand the array
        if new_capacity >= old_capacity:
            for elements in range(prime_capacity - old_capacity):
                self._buckets.append(LinkedList())

        # traverse and insert into array
        for i in range(old_capacity):
            if self._buckets[i].length() > 0:
                node = self._buckets[i]._head
                while node:
                    # Insert the value at the front, remove it from wherever it is in the linked list
                    index = self._hash_function(node.key) % prime_capacity
                    self._buckets[index].insert(node.key, node.value)
                    self._buckets[i].remove(node.key)
                    node = node.next

    def get(self, key: str):
        """
        method return the value associated with the key
        """
        # Modulo to keep the index within the bounds of the array
        index = self._hash_function(key) % self._capacity
        node = self._buckets[index]
        # if node is not empty
        if node.length() > 0:
            # check if value in linked list and return value
            value = node.contains(key)
            if value:
                return value.value

    def contains_key(self, key: str) -> bool:
        """
        Return True if the key is found in the map, False otherwise
        """
        # Hash function
        index = self._hash_function(key) % self._capacity
        node = self._buckets[index]
        # use LL contain function, if found return true else return false
        if node.contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Method removes the key from the map
        """
        # Hash function
        index = self._hash_function(key) % self._capacity
        node = self._buckets[index]
        # if key is use remove LL function
        if node.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method returns a Dynamic Array where each index contains a tuple of a key/value paid stored in the Hash Map
        """
        # create new array
        new_arr = DynamicArray()
        # traverse through buckets and list
        for i in range(self._buckets.length()):
            for node in self._buckets.get_at_index(i):
                # append key and value
                new_arr.append((node.key, node.value))
        return new_arr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    TODO: Write this implementation
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length(), hash_function_1)
    max = 0

    # map elements from da and the counts
    for elements in range(da.length()):
        # Create a counter for elements in the map
        key = da[elements]
        current = map.get(key)
        if current is not None:
            current += 1
        else:
            # Sets the initial frequency to 1
            current = 1
        # Store the key/value pair again in the map
        map.put(key, current)

        # Maintain the max value to know if we need this value as the mode
        if current > max:
            max = current
            # add mode to new_array and update max frequency
            new_array = DynamicArray()
            new_array.append(key)

        # if there are values with same frequency
        elif current == max:
            max = current
            new_array.append(key)

    return new_array, max


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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
