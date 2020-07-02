class Cart:

    def __init__(self, num):
        self.num = num
        self.isAssigned = False

    def assign(self):
        if self.isAssigned == False:
            self.isAssigned = True
            return 'Cart Assigned is to you', 200
        else:
            return 'Cart Already assigned to other user', 404

    def unassign(self):
        if self.isAssigned == True:
            self.isAssigned = False
            return 'Cart Unassigned Successfully', 200