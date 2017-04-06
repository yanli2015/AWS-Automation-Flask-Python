from flask import Flask, render_template, request
from maniplate_instance import launch_an_instance, terminate_an_instance

app = Flask(__name__)
app.secret_key = 'yanli_key'
fail_str = 'We are sorry, there is a machine running.'
success_str = 'Congratuations, a machine has been created successfully.'


@app.route('/index', methods=['GET'])
def control_instance():
    return render_template('index.html')


@app.route('/instance/create', methods=['POST'])
def launch_instance():
    result = launch_an_instance()
    if result:
        return success_str
    else:
        return fail_str


@app.route('/instance/delete', methods=['POST'])
def terminate_instance():
    print("***************")
    instance_id = request.form.get('id')
    print("instance_id: " + str(instance_id))
    result = terminate_an_instance(str(instance_id))
    if result:
        return 'Congratuations, a machine has been terminated successfully.'
    else:
        return 'Sorry, the terminate action is failed. -_-"'


if __name__ == "__main__":
    app.run(debug=True, port=5005, host='0.0.0.0', threaded=True)
