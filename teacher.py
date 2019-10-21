 def turn_by_deg(self, deg):
        """Rotates robot relative to it's current heading. If told -20, it
        will rotate left by 20 degrees."""
​
        # get our current angle
        current = self.get_heading()
​
        # calculate delta
        goal = current + deg
​
        # LOOP AROUND THE 360 marker
        goal %= 360
​
        # call turn to deg on the delta
        self.turn_to_deg(goal)
        
​
    def turn_to_deg(self, deg):
        """Turns to a degree relative to the gyroscope's readings. If told 20, it
        will rotate until the gyroscope reads 20."""
​
        # error check
        goal = abs(deg) % 360
        current = self.get_heading()
​
        turn = self.right  # connect it to the method without the () to activate
        if (current - goal > 0 and current - goal < 180) or \
            (current - goal < 0 and (360 - goal) + current < 180):
            turn = self.left
​
        
        # while loop - keep turning until my gyro says I'm there
        while abs(deg - self.get_heading()) > 3:
            turn(primary=70, counter=-70)
            time.sleep(.05) # avoid spamming the gyro
​
        # once out of the loop, hit the brakes
        self.stop()
        # report out to the user
        print("\n{} is close enough to {}.\n".format(self.get_heading(), deg))