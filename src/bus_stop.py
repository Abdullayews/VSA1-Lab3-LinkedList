class PassengerNode:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.next = None


class PassengerQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, name, age):
        node = PassengerNode(name, age)
        if self.rear is None:
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node
        self.size += 1

    def dequeue(self):
        if self.front is None:
            return None
        node = self.front
        self.front = node.next
        if self.front is None:
            self.rear = None
        node.next = None
        self.size -= 1
        return node

    def isEmpty(self):
        return self.front is None


class BusStop:

    PRIORITY_AGE = 65

    def __init__(self):
        self.priority = PassengerQueue()
        self.normal = PassengerQueue()

    def addPassenger(self, name, age):
        if age >= self.PRIORITY_AGE:
            self.priority.enqueue(name, age)
            return "priority"
        self.normal.enqueue(name, age)
        return "normal"

    def boardPassenger(self):
        if not self.priority.isEmpty():
            return self.priority.dequeue(), "priority"
        if not self.normal.isEmpty():
            return self.normal.dequeue(), "normal"
        return None, None

    def displayPassengers(self):
        print("PRIORITY QUEUE (65+):")
        if self.priority.isEmpty():
            print("  (empty)")
        else:
            cur = self.priority.front
            while cur is not None:
                print(f"  {cur.name} ({cur.age})")
                cur = cur.next
        print("NORMAL QUEUE:")
        if self.normal.isEmpty():
            print("  (empty)")
        else:
            cur = self.normal.front
            while cur is not None:
                print(f"  {cur.name} ({cur.age})")
                cur = cur.next

    def countPassengers(self):
        return self.priority.size + self.normal.size


def main():
    stop = BusStop()
    while True:
        print("\n1. Add Passenger\n2. Board Next Passenger\n3. Display Queues"
              "\n4. Count Passengers\n5. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            name = input("Passenger name: ")
            age = int(input("Age: "))
            kind = stop.addPassenger(name, age)
            label = "PRIORITY" if kind == "priority" else "normal"
            print(f"{name} added to the {label} queue.")
        elif choice == "2":
            p, kind = stop.boardPassenger()
            if p:
                print(f"{p.name} ({p.age}) boarded from the {kind} queue.")
            else:
                print("Bus stop is empty.")
        elif choice == "3":
            stop.displayPassengers()
        elif choice == "4":
            print("Passengers waiting:", stop.countPassengers())
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
