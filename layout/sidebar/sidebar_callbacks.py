from dash import Input, Output
from upload_file import save_file, check_uploaded_file

def get_callbacks_sidebar(app):

    # Callback for showing or hiding input fields for Euler Angles
    @app.callback(
    Output('euler-hide','style'),
    Input('input-grain-ori-state','value'),
    )
    def show_hide_element(grain_orientation):
        """This function returns style value for the Euler Angle input fields. 
        The field will only be shown if the selected grain orientation value is 'Specify Euler Angles (Bunge's notation in degrees)'
        Input: Selected value in Grain orientation field
        Output: Styling of Euler Angle field"""
        if grain_orientation == "Specify Euler Angles (Bunge's notation in degrees)":
            return {'display': 'block'}
        else:
            return {'display': 'none'}

    # Callback for showing or hiding input field number of random grains
    @app.callback(
    Output('random-hide','style'),
    Input('input-grain-ori-state','value'),
    )
    def show_hide_element(grain_orientation):
        """This function returns style value for the number of random grains field. 
        The field will only be shown if the selected grain orientation value is 'Random'
        Input: Selected value in Grain orientation field
        Output: Styling of number of random grains field"""
        if grain_orientation == "Random":
            return {'display': 'block'}
        else:
            return {'display': 'none'}

    # Callback for showing or hiding file upload field
    @app.callback(
    Output('upload-hide','style'),
    Input('input-grain-ori-state','value'),
    )
    def show_hide_element(grain_orientation):
        """This function returns style value for the upload field. 
        The field will only be shown if the selected grain orientation value is 'Upload file'
        Input: Selected value in Grain orientation field
        Output: Styling of number of upload field"""
        if grain_orientation == "Upload file":
            return {'display': 'block'}
        else:
            return {'display': 'none'}

    # Callback for showing the file is uploaded successfully or not
    @app.callback(
        Output("upload-indicator", "children"),
        Output("upload-indicator", "color"),
        Output("ang-threshold-hide","style"),
        Input("uploaded-file", "filename"),
        Input("uploaded-file", "contents"),
        Input("input-grain-ori-state", "value"),
    )
    def file_upload(uploaded_filename, uploaded_file_content, selected_grain_ori_state):
        """This function returns the status of the uploaded file (successful, error, not yet uploaded).
        Input: uploaded file name, content, selected grain orientation value
        Output: Message showing the status of the uploaded file"""
        if uploaded_filename is not None and uploaded_file_content is not None:
            if selected_grain_ori_state == 'Upload file':
                if uploaded_filename.endswith('.ori'):
                    save_file(uploaded_filename, uploaded_file_content)
                    result = check_uploaded_file(uploaded_filename)
                    return result, "success", {'display': 'none'}
                elif uploaded_filename.endswith('.ang'):
                    save_file(uploaded_filename, uploaded_file_content)
                    result = check_uploaded_file(uploaded_filename)
                    return result, "success", {'display': 'block'}  
                else:
                    return "Only .ori or .ang files are allowed. Please try again.", "danger", {'display': 'none'}
            else:
                return "No uploaded files yet.", "warning", {'display': 'none'}
        else:
            return "No uploaded files yet.", "warning", {'display': 'none'}

    # Call back for showing or hiding input fields for custom loading conditions
    @app.callback(
    Output('loading-cond-hide','style'),
    Input('input-loading-state','value'),
    )
    def show_hide_element(loading_condition):
        """This function returns style value for custom values field.
        The field will only be shown if the selected loading condition value is 'Input Custom Values'
        Input: Selected value in loading condition field
        Output: Styling of custom values field"""
        if loading_condition == "Input Custom Values":
            return {'display': 'block'}
        else:
            return {'display': 'none'}