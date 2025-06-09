from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import numpy as np # linear algebra
import pandas as pd
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score

# Create your views here.
from Remote_User.models import ClientRegister_Model,Predicting_Employee_Stress,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Employee_Stress_Prediction_Type(request):
    if request.method == "POST":

        employee_id= request.POST.get('employee_id')
        department= request.POST.get('department')
        region= request.POST.get('region')
        education= request.POST.get('education')
        gender= request.POST.get('gender')
        recruitment_channel= request.POST.get('recruitment_channel')
        Training_Time= request.POST.get('Training_Time')
        age= request.POST.get('age')
        Prformance_Rating= request.POST.get('Prformance_Rating')
        Years_at_company= request.POST.get('Years_at_company')
        Working_Hours= request.POST.get('Working_Hours')
        Flexible_Timings= request.POST.get('Flexible_Timings')
        Workload_level= request.POST.get('Workload_level')
        Monthly_Income= request.POST.get('Monthly_Income')
        Work_Satisfaction= request.POST.get('Work_Satisfaction')
        Percent_salary_hike= request.POST.get('Percent_salary_hike')
        companies_worked= request.POST.get('companies_worked')
        Marital_Status= request.POST.get('Marital_Status')

        import pandas as pd
        import numpy as np
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
        df = pd.read_csv('Employee_Datasets.csv', encoding='latin-1')
        df
        df.columns

        def apply_results(results):
            if (results == 'No'):
                return 0
            elif (results == 'Yes'):
                return 1

        df['Results'] = df['Stress_status'].apply(apply_results)

        # Use a list of column names instead of a tuple
        X = df[['employee_id', 'department', 'region', 'education', 'gender', 'recruitment_channel','Training_Time', 'age', 'Prformance_Rating', 'Years_at_company',
                    'Working_Hours', 'Flexible_Timings', 'Workload_level', 'Monthly_Income','Work_Satisfaction', 'Percent_salary_hike', 'companies_worked', 'Marital_Status']]
        y = df['Results']

        print("RID")
        print(X)
        print("Results")
        print(y)

        cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))
                #X = cv.fit_transform(df['employee_id'].apply(lambda x: np.str_(X)))
        # Apply CountVectorizer to specific text columns if needed
        # Example: X = cv.fit_transform(df['department'])
        # In this case, we'll apply it to all selected columns after converting them to strings
        X = cv.fit_transform(X.astype(str).apply(' '.join, axis=1))  

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
        X_train.shape, X_test.shape, y_train.shape

        print("Naive Bayes")

        from sklearn.naive_bayes import MultinomialNB
        NB = MultinomialNB()
        NB.fit(X_train, y_train)
        predict_nb = NB.predict(X_test)
        naivebayes = accuracy_score(y_test, predict_nb) * 100
        print(naivebayes)
        print(confusion_matrix(y_test, predict_nb))
        print(classification_report(y_test, predict_nb))
        models.append(('naive_bayes', NB))


        # SVM Model
        print("SVM")
        from sklearn import svm
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))
        detection_accuracy.objects.create(names="SVM", ratio=svm_acc)

        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression
        reg = LogisticRegression(random_state=42, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))


        print("KNeighborsClassifier")

        from sklearn.neighbors import KNeighborsClassifier
        kn = KNeighborsClassifier()
        kn.fit(X_train, y_train)
        knpredict = kn.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, knpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, knpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, knpredict))

        print("Decision Tree Classifier")
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        dtcpredict = dtc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, dtcpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, dtcpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, dtcpredict))
        models.append(('DecisionTreeClassifier', dtc))
        detection_accuracy.objects.create(names="Decision Tree Classifier",ratio=accuracy_score(y_test, dtcpredict) * 100)

        print("SGD Classifier")
        from sklearn.linear_model import SGDClassifier
        sgd_clf = SGDClassifier(loss='hinge', penalty='l2', random_state=0)
        sgd_clf.fit(X_train, y_train)
        sgdpredict = sgd_clf.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, sgdpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, sgdpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, sgdpredict))
        models.append(('SGDClassifier', sgd_clf))


        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        employee_id = [employee_id]
        vector1 = cv.transform(employee_id).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if prediction == 0:
            val = 'Low Stress'
        else:
            val = 'More Stress'

        print(val)
        print(pred1)

        Predicting_Employee_Stress.objects.create(employee_id=employee_id,
department=department,
region=region,
education=education,
gender=gender,
recruitment_channel=recruitment_channel,
Training_Time=Training_Time,
age=age,
Prformance_Rating=Prformance_Rating,
Years_at_company=Years_at_company,
Working_Hours=Working_Hours,
Flexible_Timings=Flexible_Timings,
Workload_level=Workload_level,
Monthly_Income=Monthly_Income,
Work_Satisfaction=Work_Satisfaction,
Percent_salary_hike=Percent_salary_hike,
companies_worked=companies_worked,
Marital_Status=Marital_Status,
        Prediction=val)

        return render(request, 'RUser/Employee_Stress_Prediction_Type.html',{'objs': val})
    return render(request, 'RUser/Employee_Stress_Prediction_Type.html')



