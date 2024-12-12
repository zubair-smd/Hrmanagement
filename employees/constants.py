class EmployeeConstants:
    # Templates
    TEMPLATE_LIST = 'employees/employee_list.html'
    TEMPLATE_DETAIL = 'employees/employee_detail.html'
    TEMPLATE_FORM = 'employees/employee_form.html'
    TEMPLATE_DELETE = 'employees/employee_confirm_delete.html'
    
    # Actions
    ACTION_ADD = 'Add'
    ACTION_UPDATE = 'Update'
    
    # URLs
    URL_EMPLOYEE_LIST = 'employees:employee_list'
    
    # Messages
    MSG_CREATE_SUCCESS = 'Employee created successfully.'
    MSG_UPDATE_SUCCESS = 'Employee updated successfully.'
    MSG_DELETE_SUCCESS = 'Employee deleted successfully.'
    MSG_NOT_FOUND = 'Employee not found.'
    MSG_FETCH_ERROR = 'Error fetching employee list.'
    MSG_CREATE_ERROR = 'Error creating employee.'
    MSG_UPDATE_ERROR = 'Error updating employee.'
    MSG_DELETE_ERROR = 'Error deleting employee.'
    MSG_FORM_ERRORS = 'Please correct the form errors.'
    MSG_FORM_DISPLAY_ERROR = 'Error displaying form.'
    MSG_DELETE_CONFIRM_ERROR = 'Error displaying delete confirmation.'