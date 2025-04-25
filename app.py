from flask import Flask,render_template,session,flash,redirect,request,send_from_directory,url_for
import mysql.connector, os
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from datetime import datetime
import time
app=Flask(__name__)
app.config['SECRET_KEY']='attendance system'

def data_base():
    db = mysql.connector.connect(host="localhost",port='3307', user="root", passwd="", database="leaf_data")
    cur=db.cursor()
    return db,cur


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('services.html')


@app.route('/signin', methods=['POST','GET'])
def signin():
    if request.method=='POST':
        useremail = request.form['userEmail'] 
        password = request.form['userPassword']

        db,cur=data_base()
        sql="select * from users where user_Email='"+useremail+"' and Password='"+password+"'"
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        if data==[]:
            flash("Invalid data entered","danger")
            return render_template('contact.html')
        else:
          
            session['useremail']=useremail
            session['username']=data[0][2]
            flash("welcome ","success")
            return render_template('userdash.html')
         
    return render_template('contact.html')

@app.route('/contact',methods=["POST","GET"])
def contact():
    print('ggdsasd')
    if request.method=='POST':
        print('hai')
        username=request.form['name']
        useremail = request.form['email']       
        password = request.form['pwd']
        mobile = request.form['ph']
        address = request.form['addr']
        db,cur=data_base()
        sql="select * from users where user_Email='%s' "%(useremail)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        if data==[]:
            sql = "insert into users(user_Name,user_Email,Password,user_Phone,user_Addr) values(%s,%s,%s,%s,%s)"
            val=(username,useremail,password,mobile,address)
            cur.execute(sql,val)
            db.commit()
            flash("User registered Successfully","success")
            return render_template("contact.html")
        else:
            flash("Details already Exists","warning")
            return render_template("contact.html")
        
    return render_template('contact.html')

@app.route('/userdash')
def userdash():
    return render_template('userdash.html')

@app.route("/upload", methods=["POST","GET"])
def upload():
    if request.method=='POST':
        myfile=request.files['file']
        fn=myfile.filename
        mypath=os.path.join('images/', fn)
        myfile.save(mypath)
        accepted_formated=['jpg','png','jpeg','jfif','JPG']
        if fn.split('.')[-1] not in accepted_formated:
            flash("Image formats only Accepted","Danger")
            return render_template("upload.html")
        base_path = os.path.dirname(os.path.abspath(__file__))
        model_path=os.path.join(base_path, "models", "mobilenet.h5")

        new_model = load_model(model_path)
        print(new_model)
        test_image = image.load_img(mypath, target_size=(256, 256))

        test_image = image.img_to_array(test_image)
        test_image = test_image/255
        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)
        print(result)
        classes=['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 
                'Blueberry___healthy', 'Cherry_(including_sour)___healthy', 
                'Cherry_(including_sour)___Powdery_mildew', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
                'Corn_(maize)___Common_rust_', 'Corn_(maize)___healthy', 'Corn_(maize)___Northern_Leaf_Blight',
                'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___healthy', 
                'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Orange___Haunglongbing_(Citrus_greening)', 
                'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
                'Potato___Early_blight', 'Potato___healthy', 'Potato___Late_blight', 'Raspberry___healthy', 
                'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___healthy', 'Strawberry___Leaf_scorch', 
                'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___healthy', 'Tomato___Late_blight', 
                'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
                'Tomato___Target_Spot', 'Tomato___Tomato_mosaic_virus', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus']
        print(classes[np.argmax(result)])
        prediction=classes[np.argmax(result)]
        if prediction == "Apple___Apple_scab":
            causes = "Fungus in wet conditions."
            remedies = "Apply fungicides, prune infected parts, maintain orchard sanitation."
            organic = "organic solutions, consider using neem oil or copper-based fungicides"
            Inorganic = " Inorganic solutions include chemical fungicides like captan or myclobutanil."

        elif prediction == "Apple___Black_rot":
            causes = "Fungus through wounds."
            remedies = "Prompt pruning, fungicides during the season, proper orchard hygiene."
            organic = "Use neem oil spray regularly to prevent and manage black rot."
            Inorganic = "Apply copper-based fungicides as a preventive measure against black rot."

        elif prediction == "Apple___Cedar_apple_rust":
            causes = "Fungus spread from junipers."
            remedies = "Apply fungicides, remove junipers, enhance air circulation."
            organic = "Pruning infected branches and applying neem oil."
            Inorganic = "Spraying affected trees with copper fungicides"

        elif prediction == "Apple___healthy":
            causes = "No disease."
            remedies = "Regular pruning, sanitation, vigilant disease monitoring."
            organic = " "
            Inorganic = " "

        elif prediction == "Blueberry___healthy":
            causes = "No disease."
            remedies = "Effective crop management, soil care, pest control."
            organic = " "
            Inorganic = " "

        elif prediction == "Cherry_(including_sour)___healthy":
            causes = "No disease."
            remedies = "Proper orchard care, regular pruning, disease monitoring."
            organic = " "
            Inorganic = " "

        elif prediction == "Cherry_(including_sour)___Powdery_mildew":
            causes = "Fungus in humid conditions."
            remedies = "Fungicides, improved ventilation, prompt pruning."
            organic = "Milk solution: Diluted milk (1 part milk to 9 parts water) sprayed on the affected plants can help suppress powdery mildew growth due to its antifungal properties."
            Inorganic = " Sulfur-based fungicides are effective against powdery mildew and can be applied to cherry trees according to label instructions."

        elif prediction == "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot":
            causes = "Fungus (Cercospora spp.)."
            remedies = "Crop rotation, resistant varieties, fungicides."
            organic = "Utilize neem oil spray or copper-based fungicides"
            Inorganic = "Apply chemical fungicides containing chlorothalonil or azoxystrobin."


        elif prediction == "Corn_(maize)___Common_rust_":
            causes = "Fungus (Puccinia spp.)."
            remedies = "Resistant varieties, fungicides, good field hygiene."
            organic = "Utilize neem oil or a garlic-chili pepper spray."
            Inorganic = "Apply copper-based fungicides"

        elif prediction == "Corn_(maize)___healthy":
            causes = "No disease."
            remedies = "Crop rotation, proper field management."
            organic = " "
            Inorganic = " "

        elif prediction == "Corn_(maize)___Northern_Leaf_Blight":
            causes = "Fungus (Exserohilum turcicum)."
            remedies = "Resistant varieties, preventive fungicides, sanitation."
            organic = "Crop rotation with non-host plants, intercropping with legumes, using compost or manure for soil enrichment, applying neem oil or garlic extract as natural fungicides."
            Inorganic = "Foliar application of copper-based fungicides, spraying with synthetic fungicides like chlorothalonil or mancozeb."

        elif prediction == "Grape___Black_rot":
            causes = "Fungus in wet conditions."
            remedies = "Pruning, fungicides during the season, vineyard hygiene."
            organic = "Utilize a mixture of neem oil and baking soda sprayed on affected plants. Regularly prune to enhance air circulation and sunlight exposure, minimizing damp conditions favorable for the disease."
            Inorganic = " Apply copper-based fungicides according to label instructions to control the spread of the disease."

        elif prediction == "Grape___Esca_(Black_Measles)":
            causes = "Fungus through wounds."
            remedies = "Pruning infected vines, systemic fungicides."
            organic = "Implementing cultural practices like proper pruning, improving soil health with compost, and using organic fungicides like neem oil."
            Inorganic = "Applying copper-based fungicides for control."

        elif prediction == "Grape___healthy":
            causes = "No disease."
            remedies = "Regular pruning, vigilant monitoring, disease-resistant varieties."
            organic = " "
            Inorganic = " "

        elif prediction == "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)":
            causes = "Fungus (Isariopsis spp.)."
            remedies = "Pruning, fungicides, vineyard sanitation."
            organic = "Regular application of neem oil or copper-based fungicides."
            Inorganic = "Fungicides containing chemicals like chlorothalonil or mancozeb."

        elif prediction == "Orange___Haunglongbing_(Citrus_greening)":
            causes = "Bacteria through insect vectors."
            remedies = "Remove infected trees, apply antibiotics, control vectors."
            organic = "Emphasize soil health through composting, utilizing neem oil, and employing biocontrol agents like beneficial nematodes."
            Inorganic = " Implementing copper-based fungicides and bactericides for disease management."

        elif prediction == "Peach___Bacterial_spot":
            causes = "Bacteria (Xanthomonas spp.)."
            remedies = "Prune, copper-based sprays, orchard sanitation."
            organic = "Copper-based fungicides, neem oil, and biocontrol agents."
            Inorganic = "Copper sulfate-based sprays."

        elif prediction == "Peach___healthy":
            causes = "No disease."
            remedies = "Proper orchard management, pruning, sanitation."
            organic = " "
            Inorganic = " "

        elif prediction == "Pepper,_bell___Bacterial_spot":
            causes = "Bacteria (Xanthomonas spp.)."
            remedies = "Resistant varieties, copper-based sprays, field hygiene."
            organic = "mplement crop rotation, use resistant varieties, apply neem oil or copper-based fungicides."
            Inorganic = "Apply copper-based bactericides or chemical fungicides approved for organic production."

        elif prediction == "Pepper,_bell___healthy":
            causes = "No disease."
            remedies = "Proper crop care, irrigation, pest control, resistant varieties."
            organic = " "
            Inorganic = " "

        elif prediction == "Potato___Early_blight":
            causes = "Fungus (Alternaria solani)."
            remedies = "Crop rotation, fungicides, proper field hygiene."
            organic = "Implement crop rotation, use neem oil as a natural fungicide, apply compost tea as a foliar spray."
            Inorganic = "Apply copper-based fungicides such as Bordeaux mixture or copper hydroxide formulations."

        elif prediction == "Potato___healthy":
            causes = "No disease."
            remedies = "Crop rotation, proper field management."
            organic = " "
            Inorganic = " "


        elif prediction == "Potato___Late_blight":
            causes = "Oomycete (Phytophthora infestans)."
            remedies = "Fungicides, avoid wet conditions, crop rotation."
            organic = "Use copper-based fungicides or neem oil"
            Inorganic = "Apply chemical fungicides containing chlorothalonil or mancozeb"

        elif prediction == "Raspberry___healthy":
            causes = "No disease."
            remedies = "Proper care, pruning, pest control."
            organic = " "
            Inorganic = " "

        elif prediction == "Soybean___healthy":
            causes = "No disease."
            remedies = "Crop rotation, proper field management."
            organic = " "
            Inorganic = " "


        elif prediction == "Squash___Powdery_mildew":
            causes = "Fungus (Podosphaera spp.)."
            remedies = "Fungicides, proper spacing, remove infected plants."
            organic = "Neem oil spray or milk solution (diluted with water)"
            Inorganic = "Potassium bicarbonate spray"

        elif prediction == "Strawberry___healthy":
            causes = "No disease."
            remedies = "Proper care, disease-resistant varieties, pest control."
            organic = " "
            Inorganic = " "


        elif prediction == "Strawberry___Leaf_scorch":
            causes = "Fungus (Diplocarpon earlianum)."
            remedies = "Fungicides, prune infected leaves, proper irrigation."
            organic = "Applying neem oil or a solution of garlic and water can help manage strawberry leaf scorch."
            Inorganic = "Using copper fungicides can be effective in controlling strawberry leaf scorch."

        elif prediction == "Tomato___Bacterial_spot":
            causes = "Bacteria (Xanthomonas spp.)."
            remedies = "Resistant varieties, copper-based sprays, crop rotation."
            organic = "Neem oil spray mixed with garlic extract"
            Inorganic = "Copper-based fungicides."

        elif prediction == "Tomato___Early_blight":
            causes = "Fungus (Alternaria solani)."
            remedies = "Fungicides, proper spacing, remove infected leaves."
            organic = "Apply neem oil or potassium bicarbonate spray regularly to control fungal growth"
            Inorganic = "Use copper-based fungicides according to label instructions for effective control."

        elif prediction == "Tomato___healthy":
            causes = "No disease."
            remedies = "Crop rotation, proper care, disease-resistant varieties."
            organic = " "
            Inorganic = " "


        elif prediction == "Tomato___Late_blight":
            causes = "Oomycete (Phytophthora infestans)."
            remedies = "Fungicides, avoid wet conditions, proper ventilation."
            organic = "Use copper-based fungicides or apply a solution of neem oil to control Tomato Late Blight."
            Inorganic = "Apply synthetic fungicides such as chlorothalonil or mancozeb to manage Tomato Late Blight."
            
        elif prediction == "Tomato___Leaf_Mold":
            causes = "Fungus (Fulvia fulva)."
            remedies = "Fungicides, proper ventilation, remove infected leaves."
            organic = "Use a mixture of neem oil and water sprayed on the affected plants"
            Inorganic = "Apply copper-based fungicides according to label instructions."

        elif prediction == "Tomato___Septoria_leaf_spot":
            causes = "Fungus (Septoria lycopersici)."
            remedies = "Fungicides, prune infected leaves, proper irrigation."
            organic = "Apply neem oil or copper fungicide."
            Inorganic = "Apply chemical fungicides such as chlorothalonil or mancozeb."

        elif prediction == "Tomato___Spider_mites Two-spotted_spider_mite":
            causes = "Two-spotted spider mite (Tetranychus urticae)."
            remedies = "Predatory mites, insecticidal soaps, proper humidity control."
            organic = "Introduce beneficial insects like ladybugs or lacewings to prey on spider mites."
            Inorganic = "Apply a neem oil or insecticidal soap spray to control spider mite infestation."

        elif prediction == "Tomato___Target_Spot":
            causes = "Fungus (Corynespora cassiicola)."
            remedies = "Fungicides, prune infected leaves, proper field hygiene."
            organic = "Utilize neem oil or copper-based fungicides."
            Inorganic = "Apply chemical fungicides like chlorothalonil or mancozeb."

        elif prediction == "Tomato___Tomato_mosaic_virus":
            causes = "Virus (Tomato mosaic virus)."
            remedies = "Remove infected plants, control aphids, use virus-free seeds."
            organic = "Implement crop rotation, use resistant tomato varieties, employ neem oil or garlic spray as natural repellents."
            Inorganic = "Apply copper-based fungicides or chemical sprays like mancozeb for control."

        elif prediction == "Tomato___Tomato_Yellow_Leaf_Curl_Virus":
            causes = "Virus (Tomato yellow leaf curl virus)."
            remedies = "Use resistant varieties, control whiteflies, remove infected plants."
            organic = "Implement crop rotation, use resistant/tolerant tomato varieties, employ reflective mulches, encourage beneficial insects, and apply neem oil or garlic spray."
            Inorganic = "Utilize chemical pesticides such as imidacloprid or spinosad, following recommended application rates and safety precautions"
            

        else:
            causes = "Class not recognized."
            remedies = "Please provide causes and remedies for this class."
            organic = " Please provide organic solution for this class"
            Inorganic = "Please provide Inorganic for this class."

            


        return render_template("result.html",image_name=fn, text=prediction,causes=causes,remedies=remedies,organic=organic,Inorganic=Inorganic)
    return render_template('upload.html')
@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


if __name__=='__main__':
    app.run(debug=True)