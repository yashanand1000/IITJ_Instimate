
# # import datetime as dt
# from typing import Any, Text, Dict, List

# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher








# class ActionCourseProf(Action):

#     def name(self) -> Text:
#         return "action_course_prof"
    
#     def run(self,dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         dispatcher.utter_message(text="Rajendra Nagar")
        
        
#         return[]

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import mysql.connector
from mysql.connector import MySQLConnection
from rasa_sdk.types import DomainDict

class MySQLConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MySQLConnector, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.cnx = None

    def get_connection(self) -> MySQLConnection:
        if not self.cnx:
            host = "35.200.181.43"
            user = "admin"
            password = "admin@instimate"
            database = "IIT_JODHPUR"

            config = {
                'user': user,
                'password': password,
                'host': host,
                'database': database
            }

            self.cnx = mysql.connector.connect(**config)

        return self.cnx

# Create a singleton instance of the MySQLConnector class
mysql_connector = MySQLConnector()

class ActionProvideCourseInfo(Action):
    def name(self) -> Text:
        return "action_provide_course_info"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        course = tracker.get_slot("course")

        # Check if course slot is not filled
        if not course:
            # Prompt user for course slot
            dispatcher.utter_message("Which course are you interested in?")
            return []

        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch course information
        cursor = cnx.cursor()
        query = "SELECT * FROM courses WHERE course_name = %s"
        cursor.execute(query, (course,))
        result = cursor.fetchone()

        if result:
            # Extract the relevant information from the query result

            
            course_code, course_level, course_name, department_name, offered_for_program, course_type, course_structure, course_credits, course_prerequisites, course_antirequisites = result

            # Example response
            dispatcher.utter_message(text=f"The course code for {course} is {course_code}.")
            dispatcher.utter_message(text=f"The {course} course is a {course_level} level course.")
            dispatcher.utter_message(text=f"The {course} course is offered for the {offered_for_program} program.")
            dispatcher.utter_message(text=f"The {course} course is a {course_type} course.")
            dispatcher.utter_message(text=f"The {course} course structure is: {course_structure}.")
            dispatcher.utter_message(text=f"The {course} course is worth {course_credits} credits.")
            dispatcher.utter_message(text=f"The prerequisites for {course} are: {course_prerequisites}.")
            dispatcher.utter_message(text=f"The antirequisites for {course} are: {course_antirequisites}.")
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find information about the course {course}.")

        # Close the database connection
        cursor.close()

        return []


class ActionProvideCourseProfessors(Action):
    def name(self) -> Text:
       return "action_provide_course_professors"


    def run(
       self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
       course_name = tracker.get_slot("course")
       cnx = mysql_connector.get_connection()
       # Execute the query to fetch course professors
       cursor = cnx.cursor()
       query = "SELECT course_faculty FROM courses WHERE course_name  = %s"
       cursor.execute(query, (course_name,))
      
       results = cursor.fetchone()


       if results:
           # Extract the professor names from the query results


           professor = results[0]
           # Example response
           dispatcher.utter_message(text=f"The {course_name} course is taught by Prof. {professor}")
          
       else:
           dispatcher.utter_message(
               text=f"Sorry, I couldn't find any information about professors teaching {course_name}.")
          
       # Close the database connection
       cursor.close()

       return []

class ActionProvideDepartmentInfo(Action):
    def name(self) -> Text:
        return "action_provide_department_info"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        department = tracker.get_slot("department")

        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch department information
        cursor = cnx.cursor()
        query = "SELECT * FROM departments WHERE department_name = %s"
        cursor.execute(query, (department,))
        result = cursor.fetchone()

        if result:
            # Extract the relevant information from the query result
            department_id, department_name, department_hod, department_about, department_webpage, department_email, department_telephone = result

            # Example response
            dispatcher.utter_message(text=f"The {department} department is headed by {department_hod}.")
            dispatcher.utter_message(text=f"About {department} department: {department_about}.")
            dispatcher.utter_message(text=f"For more information, visit the department webpage: {department_webpage}.")
            dispatcher.utter_message(text=f"You can contact the department via email at: {department_email}.")
            dispatcher.utter_message(text=f"You can call the department at: {department_telephone}.")
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find information about the {department} department.")

        # Close the database connection
        cursor.close()

        return []

class ActionProvideProfessorInfo(Action):
    def name(self) -> Text:
        return "action_provide_professor_info"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        professor = tracker.get_slot("professor")

        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch professor information
        cursor = cnx.cursor()
        query = "SELECT * FROM faculty WHERE faculty_name LIKE %s"
        cursor.execute(query, (professor,))
        result = cursor.fetchone()

        if result:
            # Extract the relevant information from the query result
            faculty_id, department_id, faculty_name, faculty_type, designation, email, phone_no, phd, photo = result

            # Example response
            dispatcher.utter_message(text=f"{faculty_name} is a {faculty_type} in the department.")
            dispatcher.utter_message(text=f"{faculty_name}'s designation is {designation}.")
            dispatcher.utter_message(text=f"You can reach {faculty_name} via email at: {email}.")
            dispatcher.utter_message(text=f"You can contact {faculty_name} at phone number: {phone_no}.")
            dispatcher.utter_message(text=f"{faculty_name} has a Ph.D.: {phd}.")
            dispatcher.utter_message(image=photo)  # Assuming 'photo' contains the URL/path to the professor's photo
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find information about the professor {professor}.")

        # Close the database connection
        cursor.close()

        return []

class ActionProvideProjectInfo(Action):
    def name(self) -> Text:
        return "action_provide_project_info"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        department = tracker.get_slot("department")

        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch project information
        cursor = cnx.cursor()
        query = "SELECT * FROM projects WHERE department_name = %s"
        cursor.execute(query, (department,))
        result = cursor.fetchone()

        if result:
            # Extract the relevant information from the query result
            department_id, department_name, project_webpage = result

            # Example response
            dispatcher.utter_message(text=f"To know about ongoing projects in the {department_name} department, please visit the webpage: {project_webpage}.")
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find information about ongoing projects in the {department_name} department.")

        # Close the database connection
        cursor.close()

        return []

class ActionProvideOngoingProjects(Action):
    def name(self) -> Text:
        return "action_provide_ongoing_projects"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch ongoing projects
        cursor = cnx.cursor()
        query = "SELECT department_name, project_webpage FROM projects"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            # Extract the project information from the query results
            projects = [f"{department_name}: {project_webpage}" for department_name, project_webpage in results]

            # Example response
            dispatcher.utter_message(text="Here are some ongoing projects:")
            dispatcher.utter_message(text="\n".join(projects))
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any ongoing projects.")

        # Close the database connection
        cursor.close()

        return []

class ActionProvidePrograms(Action):
    def name(self) -> Text:
        return "action_provide_programs"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch programs
        cursor = cnx.cursor()
        query = "SELECT program_type_id, program_name FROM ug_programs UNION SELECT program_type_id, program_name FROM pg_programs"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            # Extract the program names from the query results
            programs = ["{} - {}".format(program_type_id, program_name) for program_type_id, program_name in results]

            # Example response
            dispatcher.utter_message(text="Here are the programs offered:")
            dispatcher.utter_message(text="\n".join(programs))
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any programs.")

        # Close the database connection
        cursor.close()

        return []

# class ActionProvideProfessorResearchArea(Action):
#     def name(self) -> Text:
#         return "action_provide_professor_research_area"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         professor_name = tracker.get_slot("professor")

#         # Connect to the MySQL database
#         cnx = mysql_connector.get_connection()

#         # Execute the query to fetch professor's research area
#         cursor = cnx.cursor()
#         query = "SELECT research_areas FROM research WHERE department_id = 'CS'"
#         cursor.execute(query)
#         result = cursor.fetchone()

#         if result:
#             research_area = result[0]

#             # Example response
#             dispatcher.utter_message(text=f"{professor_name} specializes in {research_area}.")
#         else:
#             dispatcher.utter_message(text=f"Sorry, I couldn't find any information about {professor_name}.")

#         # Close the database connection
#         cursor.close()

#         return []

class ActionProvideProfessorEducation(Action):
    def name(self) -> Text:
        return "action_provide_professor_education"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        professor_name = tracker.get_slot("professor")

        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch professor's education details
        cursor = cnx.cursor()
        query = "SELECT faculty_phd from faculty where faculty_name LIKE %s"
        cursor.execute(query, (professor_name,))
        result = cursor.fetchone()

        if result:
            phd = result[0]

            # Example response
            dispatcher.utter_message(text=f"Ph.D. from : {phd}")
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find any information about {professor_name}.")

        # Close the database connection
        cursor.close()

        return []

class ActionProvideCourseType(Action):
    def name(self) -> Text:
        return "action_provide_course_type"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        course = tracker.get_slot("course")

        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch course type
        cursor = cnx.cursor()
        query = "SELECT course_type FROM courses WHERE course_name = %s"
        cursor.execute(query, (course,))
        result = cursor.fetchone()

        if result:
            course_type = result[0]

            # Example response
            dispatcher.utter_message(text=f"The course type of {course} is {course_type}.")
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find any information about {course}.")

        # Close the database connection
        cursor.close()

        return []

# class ActionProvideCourseStructure(Action):
#     def name(self) -> Text:
#         return "action_provide_course_structure"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         course_code = tracker.get_slot("coursecode")

#         # Connect to the MySQL database
#         cnx = mysql_connector.get_connection()

#         # Execute the query to fetch course structure
#         cursor = cnx.cursor()
#         query = "SELECT course_structure FROM courses WHERE course_code = %s"
#         cursor.execute(query, (course_code,))
#         result = cursor.fetchone()

#         if result:
#             course_structure = result[0]

#             # Example response
#             dispatcher.utter_message(text=f"The course structure of {course_code} is as follows:")
#             dispatcher.utter_message(text=course_structure)
#         else:
#             dispatcher.utter_message(text=f"Sorry, I couldn't find any information about {course_code}.")

#         # Close the database connection
#         cursor.close()

#         return []
class ActionProvideCourseStructure(Action):
    def name(self) -> Text:
        return "action_provide_course_structure"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        course = tracker.get_slot("course")

        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch course structure
        cursor = cnx.cursor()
        query = "SELECT course_structure FROM courses WHERE course_name = %s"
        cursor.execute(query, (course,))
        result = cursor.fetchone()

        if result:
            course_structure = result[0]

            # Example response
            dispatcher.utter_message(text=f"The course structure of {course} is as follows:")
            dispatcher.utter_message(text=course_structure)
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find any information about {course}.")

        # Close the database connection
        cursor.close()

        return []

class ActionProvideCourseOfferedFor(Action):
    def name(self) -> Text:
        return "action_provide_course_offered_for"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        course = tracker.get_slot("course")

        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch programs for which the course is offered
        cursor = cnx.cursor()
        print(course)
        query = "SELECT offered_for_program FROM courses WHERE course_name LIKE %s"

        cursor.execute(query, (course,))
        results = cursor.fetchall()

        if results:
            # Extract the program names from the query results
            programs = [offered_for_program for offered_for_program, in results]

            # Example response
            dispatcher.utter_message(text=f"{course} is offered for the following programs:")
            dispatcher.utter_message(text="\n".join(programs))
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find any information about {course}.")

        # Close the database connection
        cursor.close()

        return []

class ActionProvideCoursePrerequisites(Action):
    def name(self) -> Text:
        return "action_provide_course_prerequisites"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        course_code = tracker.get_slot("coursecode")
        course = tracker.get_slot("course")

        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch course prerequisites
        
        cursor = cnx.cursor()
        query = "SELECT course_prerequisites FROM courses WHERE course_code = %s"
        cursor.execute(query, (course_code,))
        result = cursor.fetchone()

        if result:
            course_prerequisites = result[0]

            # Example response
            dispatcher.utter_message(text=f"The prerequisites for {course_code} are:")
            dispatcher.utter_message(text=course_prerequisites)
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find any information about {course_code}.")

        # Close the database connection
        cursor.close()

        return []

class ActionProvideCourseCode(Action):
    def name(self) -> Text:
        return "action_provide_course_code"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        course_name = tracker.get_slot("course")

        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        # Execute the query to fetch course code
        cursor = cnx.cursor()
        query = "SELECT course_code FROM courses WHERE course_name = %s"
        cursor.execute(query, (course_name,))
        result = cursor.fetchone()

        if result:
            course_code = result[0]

            # Example response
            dispatcher.utter_message(text=f"The course code for {course_name} is {course_code}.")
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find any information about {course_name}.")

        # Close the database connection
        cursor.close()

        return []

class ActionProvideCoursesOffered(Action):
    def name(self) -> Text:
        return "action_provide_courses_offered"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # Connect to the MySQL database
        cnx = mysql_connector.get_connection()

        department = tracker.get_slot("department")

        # Execute the query to fetch all courses offered
        cursor = cnx.cursor()
        query = "SELECT course_code, course_name FROM courses where department_name = %s"
        cursor.execute(query, (department,))
        results = cursor.fetchall()

        if results:
            # Extract the course information from the query results
            courses = [f"{course_code}: {course_name}" for course_code, course_name in results]

            # Example response
            dispatcher.utter_message(text="Here are the courses offered by the department {department} :")
            dispatcher.utter_message(text="\n".join(courses))
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any courses.")

        # Close the database connection
        cursor.close()

        return []


