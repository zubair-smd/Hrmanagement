# employees/constants.py

class EmployeeConstants:
    # URLs
    URL_EMPLOYEE_LIST = 'employees:employee_list'

    # Templates
    TEMPLATE_LIST = 'employees/employee_list.html'
    TEMPLATE_FORM = 'employees/employee_form.html'
    TEMPLATE_DELETE = 'employees/employee_confirm_delete.html'

    # Form Actions
    ACTION_ADD = 'Add'
    ACTION_UPDATE = 'Update'

    # Messages
    MSG_NOT_FOUND = "Employee not found."
    MSG_CREATE_SUCCESS = "Employee created successfully."
    MSG_UPDATE_SUCCESS = "Employee updated successfully."
    MSG_DELETE_SUCCESS = "Employee deleted successfully."
    MSG_FORM_ERRORS = "Please correct the errors below."
    MSG_FETCH_ERROR = "Unable to fetch employee list. Please try again."
    MSG_CREATE_ERROR = "An error occurred while creating the employee."
    MSG_UPDATE_ERROR = "An error occurred while updating the employee."
    MSG_DELETE_ERROR = "An error occurred while deleting the employee."
    MSG_FORM_DISPLAY_ERROR = "Unable to display employee creation form."
    MSG_UPDATE_FORM_ERROR = "Unable to display employee update form."
    MSG_DELETE_CONFIRM_ERROR = "Unable to display delete confirmation."