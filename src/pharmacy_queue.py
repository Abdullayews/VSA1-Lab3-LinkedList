class CustomerNode:

    def __init__(self, name, medication):
        self.name = name
        self.medication = medication
        self.next = None


class PharmacyQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def addCustomer(self, name, medication):
        node = CustomerNode(name, medication)
        if self.rear is None:
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node
        self.size += 1
        return node

    def serveCustomer(self):
        if self.front is None:
            return None
        node = self.front
        self.front = node.next
        if self.front is None:
            self.rear = None
        node.next = None
        self.size -= 1
        return node

    def displayQueue(self):
        if self.front is None:
            print("Queue is empty.")
            return
        print("FRONT")
        cur = self.front
        while cur is not None:
            print(f"  {cur.name} - {cur.medication}")
            cur = cur.next
        print("REAR")

    def countCustomers(self):
        return self.size


def main():
    q = PharmacyQueue()
    while True:
        print("\n1. Add Customer\n2. Serve Next Customer\n3. Display Queue"
              "\n4. Count Customers\n5. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            name = input("Customer name: ")
            medication = input("Medication name: ")
            q.addCustomer(name, medication)
            print("Customer added to the queue.")
        elif choice == "2":
            c = q.serveCustomer()
            if c:
                print(f"{c.name} received {c.medication}.")
            else:
                print("Queue is empty.")
        elif choice == "3":
            q.displayQueue()
        elif choice == "4":
            print("Customers in queue:", q.countCustomers())
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
