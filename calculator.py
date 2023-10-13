
class OptionsValidation(): 
    """
    The purpose of this class is to manage the different types of possible options, 
    propose menus and validate the responses by input.
    """

    def __init__(self, sentence: str, its_question: bool=False) -> None:
        self.sentence = sentence.capitalize()
        if its_question:
            self.sentence = "¿{}?".format(sentence)
    
    def capture_number_option(self, options_list:list) -> int:
        """
        This method captures a list of strings, which then displays them in a menu 
        of multiple numerical options. validates that a correct option is entered.
        :param option_list: List of strings
        :return: int with number option capturated and validated
        """
        print(self.sentence)
        while True:
            # all options are printed with numbers
            for i in range(len(options_list)):
                print("{}. {}".format(i+1, str(options_list[i]).capitalize()))
            print("--------------------------------------------------")
            print("")
            option = input("Answer with a number please: ")
            print("")
            try:
                number = int(option)
                if number > len(options_list) or number <= 0:
                    raise ValueError
                return number
            except ValueError:
                print("--------------------------------------------------")
                print("Wrong option, Please enter one of the following option numbers: ")
                print("")
    
    def capture_number_answer(self) -> float:
        """
        This method It validates that the option entered is a correct float, 
        otherwise it requests the data again until it is correct.
        :return: float with number option capturated and validated
        """
        print(self.sentence)
        while True:
            option = input("Answer: ")     
            try:
                result = float(option)
                return result
            except ValueError:
                print("--------------------------------------------------")
                print("Wrong option, Please enter correct number: ")
                print("")
    
    def capture_str_answer(self) -> str:
        """
        This method It validates that the option entered is a correct string, 
        otherwise it requests the data again until it is correct.
        :return: string with number option capturated and validated
        """
        print(self.sentence)
        while True:
            option = input("Answer: ")
            try: 
                number = int(option)
                print("--------------------------------------------------")
                print("Wrong option, you enter a number. Please enter correct string: ")
                print("")
            except ValueError:
                return str(option)


class UsersCalculator():
    """
    This class is responsible for generating a menu in which the user can add several expenses, 
    and several users with their different contributions. In the end the user can generate 
    a calculation to know if people who did not contribute or contributed less money owe money
    to the other people who covered their expenses.
    """
    def __init__(self) -> None:
        self.reestart_data()

    def get_the_expenses(self) -> None:
        """
        This method obtains the expenses and their descriptions.
        """
        while True:
            expense = OptionsValidation("Plese Add the cost of expense").capture_number_answer()
            description = OptionsValidation("Plese Add the description from expense").capture_str_answer()
            confirm_sentence = "Plese confirm. value: {}, description: {}".format(expense, description)
            confirm_options = ["confirm", "reinsert"]
            confirmation = OptionsValidation(confirm_sentence).capture_number_option(confirm_options)
            if confirmation == 1:
                self.expenses_description_array.append([expense, description])
                options = ["yes", "no"]
                result = OptionsValidation("Do you add another expense", True).capture_number_option(options)
                if result == 2:
                    break
    
    def list_expenses(self) -> None:
        """
        This method lists all expenses.
        """
        if not self.expenses_description_array:
            print ("Expenses have not yet been recorded.")
            print("")
        else:
            for expense in self.expenses_description_array:
                print("Cost: ${}".format(expense[0]))
                print("Description: {}".format(expense[1]))
                print("--------------------------------------------------")
                print("")
    
    def get_users(self) -> None:
        """
        This method obtains the users and their contributions.
        """
        while True:
            name = OptionsValidation("Plese Add the name from user").capture_str_answer()
            contribution = OptionsValidation("contribution of this person").capture_number_answer()
            confirm_sentence = "Plese confirm. Name: {}, contribution: ${}".format(name, contribution)
            confirm_options = ["confirm", "reinsert"]
            confirmation = OptionsValidation(confirm_sentence).capture_number_option(confirm_options)
            if confirmation == 1:
                self.users_money_array[name] = contribution
                options = ["yes", "no"]
                result = OptionsValidation("Do you add another user", True).capture_number_option(options)
                if result == 2:
                    break
    
    def list_users(self) -> None:
        """
        This method lists all users.
        """
        if not self.users_money_array:
            print ("Users have not yet been recorded.")
            print("")
        else:
            for user in self.users_money_array.keys():
                print("User Name: {}".format(str(user).capitalize()))
                print("Contribution: ${}".format(self.users_money_array[user]))
                print("--------------------------------------------------")
                print("")

    def generate_user_balance(self, payment_per_user: float) -> dict:
        """
        This method generates a dictionary that makes a balance between what 
        each user had to pay
        :param payment_per_user: float which represents what each user must pay
        :return: returns a dictionary with the balance.
        """
        user_balance_dict = {}
        for user in self.users_money_array.keys():
            balance = self.users_money_array[user] - payment_per_user
            user_balance_dict[user] = balance
        return user_balance_dict
    
    def users_posivite_balance(self, user_balance_dict: dict) -> int:
        """
        This method validates all users who have a positive balance 
        between what each one should contribute and what they contributed
        :param user_balance_dict: dictionary with balance sheets
        :return: int with the number of users with positive balance
        """
        count = 0
        for user in user_balance_dict.keys():
            if user_balance_dict[user] > 0: 
                count += 1
        return count


    def calculation(self, user_balance_dict:dict, evaluated_user:str = None, 
                    contributions_dict:dict = {}, amount:str = None) -> dict:
        """
        This is a recursive method that validates among the list of users who 
        need other users to contribute to reach the goal of the minimum to contribute
        with the total expenses. generates debt per user towards other users.
        :param user_balance_dict: dictionary with balance sheets
        :param evaluated_user: This parameter is updated recursively as the method processes the data.
        :param contributions_dict: dictionary that fills up and returns at the end.
        :param amount: amount owed by the user that is being processed. 
                       This value is updated in the process
        """   
        for user in user_balance_dict.keys():
            # users are scanned to validate who has a negative balance
            if user_balance_dict[user] < 0 and evaluated_user == None:
                # when the first one is captured, recursion is applied by sending the key by parameter
                self.calculation(user_balance_dict, user)
            
            if user_balance_dict[user] > 0 and evaluated_user and user != evaluated_user:
                #the first user who can provide is captured
                if not amount:
                    amount_due = user_balance_dict.get(evaluated_user)
                    positive_users = self.users_posivite_balance(user_balance_dict)
                    amount = amount_due / positive_users
            
                if user_balance_dict[user] + amount >= 0:
                    # if when lending there is a positive balance, the information 
                    # is updated and saved in the dictionary to return the loan information
                    user_balance_dict[user] = user_balance_dict[user] + amount
                    user_balance_dict[evaluated_user] = user_balance_dict[evaluated_user] - amount

                    if evaluated_user not in contributions_dict:
                        contributions_dict[evaluated_user] = {user: abs(amount)}

                    else:
                        seder_dict = contributions_dict.get(evaluated_user)
                        total = seder_dict.get(user) + abs(amount) if user in seder_dict else abs(amount)
                        seder_dict[user] = total
                
                elif user_balance_dict[user] + amount < 0:
                    # if the loan results in a zero value, the information is updated 
                    # and saved in the dictionary to return the loan information.
                    user_balance_dict[evaluated_user] = user_balance_dict[evaluated_user] + user_balance_dict[user]

                    if evaluated_user not in contributions_dict:
                        contributions_dict[evaluated_user] = {user: user_balance_dict[user]}
                    else:
                        seder_dict = contributions_dict.get(evaluated_user)
                        total = seder_dict.get(user) + user_balance_dict[user] if user in seder_dict else user_balance_dict[user]
                        seder_dict[user] = total

                    user_balance_dict[user] = float(0)

        # If all users have finished visiting and the negative balance was not managed, 
        # recursion is applied to make a new tour, recalculating what should be lent 
        # taking into account that the debt has already decreased.
        if evaluated_user and user_balance_dict[evaluated_user] < 0:
            self.calculation(user_balance_dict, evaluated_user, contributions_dict)

        return contributions_dict 
    
    def payment_calculation(self) -> None:
        """
        This method validates that the calculations can be started 
        and executes the calculation function and returns the dictionary with the debts.
        """
        if not self.users_money_array or not self.expenses_description_array:
            print ("There must be a record of expenses and contributions by users. " +
                "If there is not one of the two, payment calculations cannot be obtained.")
            return
        
        contribution = sum(self.users_money_array[user] for user in self.users_money_array.keys())
        expenses = sum(expense[0] for expense in self.expenses_description_array)

        if expenses > contribution:
            print("What was spent is greater than the contributions of the users. " +
                "please add contributions or edit existing ones")
            return
    
        payment_per_user = expenses / len(self.users_money_array)
        user_balance_dict = self.generate_user_balance(payment_per_user)

        result_dict = self.calculation(user_balance_dict)
        for name in result_dict.keys():
            print("Debts of {}: ".format(str(name).upper()))
            for sub_name in result_dict[name].keys():
                print("{} must pay: ${} to {}".format(str(name).capitalize(), result_dict.get(name)[sub_name],
                                                      str(sub_name).capitalize()))
            print("--------------------------------------------------")
        print("")
    
    def reestart_data(self, print_message:bool =True) -> None:
        """
        This method deletes all user data and debts
        """
        self.users_money_array = {}
        self.expenses_description_array = []
        if print_message:
            print("The data was deleted.")
            print("--------------------------------------------------")
            print("")
        
    def run(self):
        """
        This method runs a menu in the terminal with different options to 
        run the different processes.
        """
        print("--------------------------------------------------")
        print("* * * * * WELCOME TO EXPENSES CALCULATOR * * * * *")
        print("--------------------------------------------------")
        while True:
            options = ["add expense/s", "list expenses", "add user/s", "list user", 
                       "calculate payments", "reestart data", "exit"]
            result = OptionsValidation("please select one of following options").capture_number_option(options)
            if result == 1:
                self.get_the_expenses()
            elif result == 2:
                self.list_expenses()
            elif result == 3:
                self.get_users()
            elif result == 4:
                self.list_users()
            elif result == 5:
                self.payment_calculation()
            elif result == 6:
                self.reestart_data()
            elif result == 7:
                break
                
UsersCalculator().run()
