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
    # my_check_boxes = MultiCheckboxField('Label', choices=choice_list)
    my_check_boxes = MultiCheckboxField('Label')

@app.route('/',methods=['post','get'])
def hello_world():
    form = SimpleForm()

    # overriding the choices for demo purposes (these were already set in the SimpleForm above)
    form.my_check_boxes.choices=[('one', 'One_label'), ('two', 'Two_label'), ('three', 'Three_label'), ('cherries', 'Cherries')] # this sets the total number of checkboxes


    if form.validate_on_submit():
        print(form.my_check_boxes.data)
        return render_template("success.html", data=form.my_check_boxes.data)
    else:
        print("Validation Failed")
        print(form.errors)

    # setting the initial boxes that should be checked (ordinarily u would get this through a db call)    
    form.my_check_boxes.data=['one','two'] # this checks the appropriate boxes

    return render_template('example.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)