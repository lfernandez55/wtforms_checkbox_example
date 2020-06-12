from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField

# from https://gist.github.com/doobeh/4668212

SECRET_KEY = 'development'
app = Flask(__name__)
app.config.from_object(__name__)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SimpleForm(FlaskForm):
    # create a list of value/description tuples
    choice_list =  [('one', 'One_label'), ('two', 'Two_label'), ('three', 'Three_label')]
    my_check_boxes = MultiCheckboxField('Label', choices=choice_list)
    # Alternatively, the choices could be set in the view (see how I do that below)
    # my_check_boxes = MultiCheckboxField('Label')

@app.route('/',methods=['post','get'])
def hello_world():
    # To put checks in some of the checkboxes u would make a db call to create an array.  Then you could add it like so:

    # form = SimpleForm()  
    # form.my_check_boxes.data=['one','two'] # this checks the appropriate boxes

    # While the above will put checks in two checkboxes, it will overwrite whatever came in thru the form in a post request. As a result the above approach 
    # never processes/saves the post data. You can test this by uncommenting the above two lines and commenting out the next line.  

    # Instead, we instantiate the form in the following line below.  This allows the form to be populated with ['one','two'] on the GET request which 
    # contains no form data. In contrast, on the POST request WTforms is designed to instantiate the form object with whatever came in on the POST request!  See "How Forms get data"
    # in https://wtforms.readthedocs.io/en/2.3.x/crash_course/.  
    form = SimpleForm( my_check_boxes=['one','two'])

    # overriding the choices for demo purposes (these were already set in the SimpleForm above)
    form.my_check_boxes.choices=[('one', 'One_label'), ('two', 'Two_label'), ('three', 'Three_label'), ('cherries', 'Cherries')] # this sets the total number of checkboxes


    if form.validate_on_submit():
        print(form.my_check_boxes.data)
        # Notice here the checked boxes are access with the "data" attribute
        return render_template("success.html", data=form.my_check_boxes.data)
    else:
        print("Validation Failed")
        print(form.errors)

    return render_template('example.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)