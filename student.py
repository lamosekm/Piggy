from teacher import PiggyParent
import sys
import time


class Piggy(PiggyParent):





    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 100
        self.RIGHT_DEFAULT = 100
        # PRO LEVEL
        self.SAFE_DIST = 450
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
        self.load_defaults()
        self.cornerCount = 0
        self.exit_heading = 0
        
        

    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "o": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "h": ("Hold position", self.hold_steady),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit),
                "e": ("forward", self.go),
                "s": ("left", self.go_left),
                "a": ("slightlyLeft", self.slightlyLeft),
                "f": ("right", self.go_right),
                "g": ("slighltyRight", self.slightlyRight),
                "d": ("back", self.reverse),
                "v": ("slither!", self.slither)
                }



        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''

    def go(self):
        while self.read_distance() > 150:
            self.fwd()
            time.sleep(.01)
        self.stop()

    def go_left(self):
        self.turn_by_deg(-45)

    def slightlyLeft(self):
        self.turn_by_deg(-22.5)


    def go_right(self):
        self.turn_by_deg(45)

    def slightlyRight(self):
        self.turn_by_deg(22.5)

    def reverse(self):
        self.back()
        time.sleep(.75)
        self.stop()

    def dance(self):
        # check to see it's safe
        if not self.safe_to_dance():
            print("Not cool. Not going to dance")
            return # return closes down the method
        else:
            print("It's safe to dance!")
        self.warmupPerformance() #calls warmup dance
        self.doCircles() # calls second dance
        self.reverseWheelieFail() # calls third dance
        self.waive() # calls waive method/dance
        self.wrecklessDabs() # finishes with the final performance.
        self.smallBox() # drives a box

    def safe_to_dance(self):
        """ Does a 360 distance check and returns true if safe to dance"""
        for x in range(4):
            for ang in range(self.MIDPOINT-400, self.MIDPOINT+400, 100): 
                self.servo(ang)
                time.sleep(.1)
                if self.read_distance() < 250:
                    return False
            self.turn_by_deg(90)
        return True


    def warmupPerformance(self):
        """a nice little warmup to the insane performance!"""
        self.right()
        time.sleep(2)
        self.stop()
        self.left()
        time.sleep(.25)
        self.stop()
        self.right()
        time.sleep(.25)
        self.stop()
        self.fwd()
        time.sleep(2)
        self.stop()
        self.servo(1200)
        time.sleep(1)
        self.servo(1700)
        time.sleep(1)




    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 250):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        found_something = False # trigger
        trigger_distance = 450
        count = 0
        starting_position = self.get_heading() # write down starting position
        self.right(primary=60, counter=-60)
        while self.get_heading() != starting_position:
            if self.read_distance() < trigger_distance and not found_something:
                found_something = True
                count += 1
            elif self.read_distance() > trigger_distance and found_something:
                found_something = False
                print("I have a clear view. Resetting my counter")
        self.stop()
        print("I found this many things: %d" % count)
        return count

    def quick_check(self):

        # three quick checks
        for ang in range(self.MIDPOINT-150, self.MIDPOINT+151, 150):
            self.servo(ang)
            if self.read_distance() < self.SAFE_DIST:
                return False

        #if I get to the end, this means I didn't find anything dangerous 
        return True


    def slither(self):
        """ practice a smooth veer """
        # write down where we started
        starting_direction = self.get_heading()
        # start driving forward
        self.set_motor_power(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_power(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.fwd()
        # throttle down the left motor
        for power in range(self.LEFT_DEFAULT, 50, -10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.5)
        # throttle up the left 
        for power in range(50, self.LEFT_DEFAULT + 1, 10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.1)

        # throttle down the right motor
        for power in range(self.RIGHT_DEFAULT, 50, -10):
            self.set_motor_power(self.MOTOR_RIGHT, power)
            time.sleep(.5)
        # throttle up the right 
        for power in range(50, self.RIGHT_DEFAULT + 1, 10):
            self.set_motor_power(self.MOTOR_RIGHT, power)
            time.sleep(.1)

        left_speed = self.LEFT_DEFAULT
        right_speed = self.RIGHT_DEFAULT


        # straighten out
        while self.get_heading() != starting_direction:
            # if I need to veer right
            if self.get_heading() < starting_direction:
                print("I'm too far left")
                self.set_motor_power(self.MOTOR_LEFT, 90)
                self.set_motor_power(self.MOTOR_RIGHT, 60)
            # if I need to veer left
            elif self.get_heading() > starting_direction:
                print("I'm too far right")
                self.set_motor_power(self.MOTOR_LEFT, 60)
                self.set_motor_power(self.MOTOR_RIGHT, 90)
            self.set_motor_power(self.MOTOR_LEFT, self.LEFT_DEFAULT)
            self.set_motor_power(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
            time.sleep(.1)


    def nav(self):
        self.exit_heading = self.get_heading()

        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")
        corner_count=0
        while True:
            #self.hold_steady()
            self.servo(self.MIDPOINT)
            while self.quick_check():
                self.cornerCount = 0
                self.fwd()
                time.sleep(.01)
            self.stop()
            self.cornerCount += 1
            self.shakeHeadInDisgust()
            if self.cornerCount == 4:
                self.escape()
            self.scan()
            #traversal
            left_total = 0
            left_count = 0
            right_total = 0
            right_count = 0
            for ang, dist in self.scan_data.items():
                if ang < self.MIDPOINT: 
                    right_total += dist
                    right_count += 1
                else:
                    left_total += dist
                    left_count += 1
            left_avg = left_total / left_count
            right_avg = right_total / right_count
            if left_avg > right_avg:
                self.turn_by_deg(-35)
            else:
                self.turn_by_deg(35)

    def hold_steady(self):
        angle_started_at = self.get_heading()
        while True:
            time.sleep(.1)
            current_angle = self.get_heading()
            if abs(current_angle - angle_started_at) > 15:
                self.turn_to_deg(angle_started_at)

    def path_towards_exit(self):
        self.exit_heading = self.get_heading() 
        self.turn_to_deg(self.exit_heading)
        if self.quick_check():
            return True
        else:
            self.turn_to_deg(where_I_started)
        return False
    
    def average_turn(self):
        '''robot decides where an obstacle is and turns left or right from that '''
        corner_count = 0
        corner_count += 1
        if corner_count == 3:
            self.escape()
        left_total = 0
        left_count = 0
        right_total = 0
        right_count = 0
        for ang, dist in self.scan_data.items():
            if ang < self.MIDPOINT:
                right_total += dist
                right_count +=1
            else:
                left_total += dist
                left_count += 1
        left_avg = left_total / left_count
        right_avg = right_total / right_count
        if left_avg > right_avg:
            self.turn_by_deg(-35)
        else:
            self.turn_by_deg(35)


    def escape(self):
        self.turn_by_deg(180)
        self.deg_fwd(720)
        self.turn_to_deg(self.exit_heading)

    def shakeHeadInDisgust(self):
        """Goes around an object that is in front of it"""
        if self.read_distance() < 350:
            self.servo(1000)
            time.sleep(.4)
            self.servo(2000)
            time.sleep(.4)
        self.servo(1500)

    def doCircles(self):
        """does two full circles"""
        self.right()
        time.sleep(5)
        self.stop()
    
    def reverseWheelieFail(self):
        """attempts to do a reverse wheelie... motors don't have enough power"""
        self.fwd()
        time.sleep(.1)
        self.back()
        time.sleep(.5)
        self.stop()

    def waive(self):
        """fast waives"""
        for x in range(3):
            self.servo(1000)
            time.sleep(.2)
            self.servo(2000)
            time.sleep(.2)
            self.servo(1000)
            time.sleep(.2)
            self.servo(2000)
            time.sleep(.2)
            self.servo(1000)
            time.sleep(.2)
            self.servo(2000)
            time.sleep(.2)
            self.servo(1000)
            time.sleep(.2)
            self.servo(2000)
            time.sleep(.2)
            self.stop()

    def wrecklessDabs(self):
        """does tons of dabs(7 to be exact)"""
        for x in range(7):
            self.right()
            time.sleep(.5)
            self.servo(2000)
            self.stop()
            self.back()
            time.sleep(.5)
            self.stop()
            self.left()
            time.sleep(.5)
            self.servo(1000)
            self.stop()
            self.back()
            time.sleep(.5)
            self.stop()

    def smallBox(self):
        """turns by 90 deg and drives to form a box"""
        self.fwd()
        time.sleep(.5)
        self.turn_by_deg(90)
        self.fwd()
        time.sleep(.5)
        self.turn_by_deg(90)
        self.fwd()
        time.sleep(.5)
        self.turn_by_deg(90)
        self.fwd()
        time.sleep(.5)
        self.turn_by_deg(90)
        
            
    




###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
