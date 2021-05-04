from flask import Flask , render_template,request,flash,Blueprint # render template will render the Template
from cowin_APP.forms import Data_Required
#from cowin_APP import app
#getting data from API
import requests
import datetime
import json

global output_string
global avail_date

main = Blueprint('main', __name__)
def Check_Avaibality(get_age,get_pincode):
    output_string = ""
    POST_CODE = get_pincode
    age = get_age
    # Print details flag
    print_flag = 'Y'
    numdays = 20
    base = datetime.datetime.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]
    avail_date = ""
    for INP_DATE in date_str:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(POST_CODE, INP_DATE)
        response = requests.get(URL)
        if response.ok:
            resp_json = response.json()
            # print(json.dumps(resp_json, indent = 1))
            flag = False
            if resp_json["centers"]:
                #print("Available on: {}".format(INP_DATE))
                #output_string = output_string+"Available on: {}".format(INP_DATE)+"\n"
                dt_string = INP_DATE
                if(print_flag=='y' or print_flag=='Y'):
                    for center in resp_json["centers"]:
                        for session in center["sessions"]:
                            if session["min_age_limit"] <= int(age):
                                #print("\t", center["name"])
                                center_string = "\t"+ center["name"]
                                #print("\t", center["block_name"])
                                block_string = "\t"+ center["block_name"]
                                #print("\t Price: ", center["fee_type"])
                                fee_string = "\t"+ center["fee_type"]
                                #print("\t Available Capacity: ", session["available_capacity"])
                                avai_string = "\t"+str(session["available_capacity"])
                                if(session["vaccine"] != ''):
                                    #print("\t Vaccine: ", session["vaccine"])
                                    sess_string = "\t Vaccine: "+ session["vaccine"]
                                    #print("\n\n")
                                else:
                                    sess_string = "\t No Data Available"
                                output_string = output_string+dt_string+center_string+block_string+fee_string+avai_string+sess_string+"\n\n"
                            else:
                                dt_string = INP_DATE
                                center_string = "\t No Data Available"
                                block_string = "\t No Data Available"
                                fee_string = "\t No Data Available"
                                avai_string = "\t No Data Available"
                                sess_string = "\t No Data Available"
                                output_string = output_string+center_string+block_string+fee_string+avai_string+sess_string+"\n\n"
                else:
                    #print("No available slots on {}".format(INP_DATE))
                    dt_string = INP_DATE
                    center_string = "\t No Data Available"
                    block_string = "\t No Data Available"
                    fee_string = "\t No Data Available"
                    avai_string = "\t No Data Available"
                    sess_string = "\t No Data Available"
                    output_string = output_string+dt_string+center_string+block_string+fee_string+avai_string+sess_string+"\n\n"
                    #output_string = output_string+"No available slots on {}".format(INP_DATE)+"\n\n"
    out_li = output_string.split("\n\n")
    final_out = []
    i=0
    while(i<len(out_li)):
        li1 = out_li[i].split("\t")
        while("" in li1):
            li1.remove("")
        final_out.append(li1)
        i=i+1
    return final_out

@main.route("/",methods=['GET', 'POST'])
@main.route("/home",methods=['GET', 'POST'])
def home():
    form = Data_Required()
    #if form.validate_on_submit():
    if form.validate_on_submit():
        flash(f'Data is Authentic for {form.Pincode.data}!', 'success')
        if request.method == "POST":
            get_age = request.form.get("Age")
            get_Pincode = request.form.get("Pincode")
            data = Check_Avaibality(get_age,get_Pincode)
            print(data)
        return render_template('available.html', title='Seat-Avaiblity', form=form,data=data)
    else:
        flash('Please Enter Valid Age and Indian Pincode', 'danger')
        return render_template('home.html',form=form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/available")
def Available_seat():
    return render_template('available.html', title='Seat-Avaiblity')


if __name__ == "__main__":
    app.run(debug=True)
