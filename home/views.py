from django.shortcuts import render, redirect
from theme_material_kit.forms import LoginForm, RegistrationForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
import random
from django.contrib.auth import views as auth_views
#from django.shortcuts import render
from django.http import JsonResponse
from home import models
from datetime import datetime
from django.http import HttpResponse
import csv

# Create your views here.

def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
      ip = x_forwarded_for.split(',')[0]
  else:
      ip = request.META.get('REMOTE_ADDR')
  return ip

# Authentication
def registration(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login/')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()

  context = {'form': form}
  return render(request, 'accounts/sign-up.html', context)

class UserLoginView(auth_views.LoginView):
  template_name = 'accounts/sign-in.html'
  form_class = LoginForm
  success_url = '/'

class UserPasswordResetView(auth_views.PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(auth_views.PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm

def user_logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

 
def home_page(request):
  bg_image = models.BgImage.objects.filter(type = 'BgHome').first()
  bg_image_url = bg_image.image if bg_image else None
  return render(request, 'pages/home_page.html', {'bg_image': bg_image_url,})


# Pages
def index(request):
  try: 
    bg_image = models.BgImage.objects.filter(type = 'Background').first()
    bg_image_url = bg_image.image if bg_image else None
    # print(bg_image_url)
    states = [
          "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
          "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
          "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
          "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
          "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
          "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Lakshadweep", "Delhi", "Puducherry"
      ]
    districts = {
          "Andhra Pradesh": ["Anantapur", "Chittoor", "East Godavari", "Guntur", "Krishna", "Kurnool, Prakasam", 
                            "Sri Potti Sriramulu Nellore", "Srikakulam", "Visakhapatnam", "Vizianagaram", "West Godavari", "YSR District", 
                            "Kadapa (Cuddapah)"],
          "Arunachal Pradesh": ["Anjaw"", ""Changlang", "Dibang Valley", "East Kameng", "East Siang", "Kamle", "Kra Daadi", "Kurung Kumey", 
                                "Lepa Rada", "Lohit", "Longding", "Lower Dibang Valley", "Lower Siang", "Lower Subansiri", "Namsai", 
                                "Pakke-Kessang", "Papum Pare", "Shi-Yomi", "Siang", "Tawang", "Tirap", "Upper Siang", "Upper Subansiri", 
                                "West Kameng", "West Siang"],
          "Assam": ["Baksa", "Barpeta", "Biswanath", "Bongaigaon", "Cachar", "Charaideo", "Chirang", "Darrang", "Dhemaji", 
                    "Dhubri", "Dibrugarh", "Dima Hasao", "Goalpara", "Golaghat", "Hailakandi", "Hojai", "Jorhat", "Kamrup", 
                    "Kamrup Metropolitan", "Karbi Anglong", "Karimganj", "Kokrajhar", "Lakhimpur", "Majuli", "Morigaon", "Nagaon", 
                    "Nalbari", "Sivasagar", "Sonitpur", "South Salmara-Mankachar", "Tinsukia", "Udalguri", "West Karbi Anglong "],
          "Bihar": ["Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", "Bhagalpur", "Bhojpur", "Buxar", "Darbhanga", "East Champaran (Motihari)", 
                    "Gaya", "Gopalganj", "Jamui", "Jehanabad", "Kaimur (Bhabua)", "Katihar", "Khagaria", "Kishanganj", "Lakhisarai", "Madhepura", 
                    "Madhubani", "Munger (Monghyr)", "Muzaffarpur", "Nalanda", "Nawada", "Patna", "Purnia (Purnea)", "Rohtas", "Saharsa", "Samastipur", 
                    "Saran", "Sheikhpura", "Sheohar", "Sitamarhi", "Siwan", "Supaul", "Vaishali", "West Champaran "],   
          "Chhattisgarh": ["Balod", "Baloda Bazar", "Balrampur", "Bastar", "Bemetara", "Bijapur", "Bilaspur", "Dantewada (South Bastar)", 
                            "Dhamtari", "Durg", "Gariaband", "Janjgir-Champa", "Jashpur", "Kabirdham (Kawardha)", "Kanker (North Bastar)", 
                            "Kondagaon", "Korba", "Koriya", "Mahasamund", "Mungeli", "Narayanpur", "Raigarh", "Raipur", "Rajnandgaon", "Sukma", 
                            "Surajpur", "Surguja"],
          "Goa": ["North Goa", "South Goa"],
          "Gujarat": ["Ahmedabad", "Amreli", "Anand", "Aravalli", "Banaskantha (Palanpur)", "Bharuch", "Bhavnagar", "Botad", "Chhota Udaipur", 
                      "Dahod", "Dang", "Devbhoomi Dwarka", "Gandhinagar", "Gir Somnath", "Jamnagar", "Junagadh", "Kheda (Nadiad)", "Kutch (Bhuj)", 
                      "Mahisagar", "Mehsana", "Morbi", "Narmada (Rajpipla)", "Navsari", "Panchmahal (Godhra)", "Patan", "Porbandar", "Rajkot", 
                      "Sabarkantha (Himmatnagar)", "Surat", "Surendranagar", "Tapi (Vyara)", "Vadodara", "Valsad "],  
          "Haryana": ["Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad", "Fatehabad", "Gurugram (Gurgaon)", "Hisar", "Jhajjar", "Jind", 
                      "Kaithal", "Karnal", "Kurukshetra", "Mahendragarh", "Nuh", "Palwal", "Panchkula", "Panipat", "Rewari", "Rohtak", 
                      "Sirsa", "Sonipat", "Yamunanagar "],
          "Himachal Pradesh": ["Bilaspur", "Chamba", "Hamirpur", "Kangra", "Kinnaur", "Kullu", "Lahaul and Spiti", "Mandi", "Shimla", 
                                "Sirmaur", "Solan", "Una "],  
          "Jharkhand": ["Bokaro", "Chatra", "Deoghar", "Dhanbad", "Dumka", "East Singhbhum (Jamshedpur)", "Garhwa", "Giridih", "Godda", 
                        "Gumla", "Hazaribagh", "Jamtara", "Khunti", "Koderma", "Latehar", "Lohardaga", "Pakur", "Palamu", "Ramgarh", 
                        "Ranchi", "Sahibganj", "Seraikela-Kharsawan", "Simdega", "West Singhbhum (Chaibasa)"],
          "Karnataka": ["Bagalkot", "Ballari (Bellary)", "Belagavi (Belgaum)", "Bengaluru Rural", "Bengaluru Urban", "Bidar", "Chamarajanagar", 
                        "Chikballapur", "Chikkamagaluru (Chikmagalur)", "Chitradurga", "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", 
                        "Hassan", "Haveri", "Kalaburagi (Gulbarga)", "Kodagu", "Kolar", "Koppal", "Mandya", "Mysuru (Mysore)", "Raichur", 
                        "Ramanagara", "Shivamogga (Shimoga)", "Tumakuru (Tumkur)", "Udupi", "Uttara Kannada (Karwar)", "Vijayapura (Bijapur)",
                          "Yadgir"],
          "Kerala": ["Alappuzha", "Ernakulam", "Idukki", "Kannur", "Kasaragod", "Kollam", "Kottayam", "Kozhikode", "Malappuram", "Palakkad", 
                    "Pathanamthitta", "Thiruvananthapuram", "Thrissur", "Wayanad"],
          "Madhya Pradesh": ["Agar Malwa", "Alirajpur", "Anuppur", "Ashoknagar", "Balaghat", "Barwani", "Betul", "Bhind", "Bhopal", "Burhanpur", 
                            "Chhatarpur", "Chhindwara", "Damoh", "Datia", "Dewas", "Dhar", "Dindori", "Guna", "Gwalior", "Harda", "Hoshangabad", 
                            "Indore", "Jabalpur", "Jhabua", "Katni", "Khandwa", "Khargone", "Mandla", "Mandsaur", "Morena", "Narsinghpur", 
                            "Neemuch", "Panna", "Raisen", "Rajgarh", "Ratlam", "Rewa", "Sagar", "Satna", "Sehore", "Seoni", "Shahdol",
                              "Shajapur", "Sheopur", "Shivpuri", "Sidhi", "Singrauli", "Tikamgarh", "Ujjain", "Umaria", "Vidisha"],
          "Maharashtra": ["Ahmednagar", "Akola", "Amravati", "Aurangabad", "Beed", "Bhandara", "Buldhana", "Chandrapur", "Dhule", 
                          "Gadchiroli", "Gondia", "Hingoli", "Jalgaon", "Jalna", "Kolhapur", "Latur", "Mumbai City", "Mumbai Suburban", 
                          "Nagpur", "Nanded", "Nandurbar", "Nashik", "Osmanabad", "Palghar", "Parbhani", "Pune", "Raigad", "Ratnagiri", 
                          "Sangli", "Satara", "Sindhudurg", "Solapur", "Thane", "Wardha", "Washim", "Yavatmal"],
          "Manipur": ["Bishnupur", "Chandel", "Churachand"],
          "Meghalaya": ["East Garo Hills", "East Jaintia Hills", "East Khasi Hills", "North Garo Hills", "Ribhoi", "South Garo Hills",
                        "South West Garo Hills", "South West Khasi Hills", "West Garo Hills", "West Jaintia Hills", "West Khasi Hills"],
          "Mizoram": ["Aizawl", "Champhai", "Hnahthial", "Khawzawl", "Lawngtlai", "Lunglei", "Mamit", "Saiha", "Saitual", "Serchhip"],
          "Nagaland": ["Dimapur", "Kiphire", "Kohima", "Longleng", "Mokokchung", "Mon", "Peren", "Phek", "Tuensang", "Wokha", "Zunheboto"],
          "Odisha": ["Angul", "Balangir", "Balasore", "Bargarh", "Bhadrak", "Boudh", "Cuttack", "Debagarh", "Dhenkanal", "Gajapati", 
                    "Ganjam", "Jagatsinghpur", "Jajpur", "Jharsuguda", "Kalahandi", "Kandhamal", "Kendrapara", "Kendujhar (Keonjhar)", 
                    "Khordha", "Koraput", "Malkangiri", "Mayurbhanj", "Nabarangpur", "Nayagarh", "Nuapada", "Puri", "Rayagada", 
                    "Sambalpur", "Subarnapur (Sonepur)", "Sundargarh"],
          "Punjab": ["Amritsar", "Barnala", "Bathinda", "Faridkot", "Fatehgarh Sahib", "Fazilka", "Ferozepur", "Gurdaspur", "Hoshiarpur", 
                    "Jalandhar", "Kapurthala", "Ludhiana", "Mansa", "Moga", "Muktsar", "Pathankot", "Patiala", "Rupnagar", 
                    "Sahibzada Ajit Singh Nagar (Mohali)", "Sangrur", "Shahid Bhagat Singh Nagar (Nawanshahr)", "Sri Muktsar Sahib", "Tarn Taran"],
          "Rajasthan": ["Ajmer", "Alwar", "Banswara", "Baran", "Barmer", "Bharatpur", "Bhilwara", "Bikaner", "Bundi", "Chittorgarh", "Churu", 
                        "Dausa", "Dholpur", "Dungarpur", "Hanumangarh", "Jaipur", "Jaisalmer", "Jalore", "Jhalawar", "Jhunjhunu", "Jodhpur", 
                        "Karauli", "Kota", "Nagaur", "Pali", "Pratapgarh", "Rajsamand", "Sawai Madhopur", "Sikar", "Sirohi", "Sri Ganganagar",
                          "Tonk", "Udaipur"],
          "Sikkim": ["East Sikkim", "North Sikkim", "South Sikkim", "West Sikkim"],
          "Tamil Nadu": ["Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore", "Dharmapuri", "Dindigul", "Erode", 
                        "Kallakurichi", "Kanchipuram", "Kanyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai", 
                        "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai", "Ramanathapuram", "Ranipet", "Salem", 
                        "Sivaganga", "Tenkasi", "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli", "Tirupathur", 
                        "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", "Vellore", "Viluppuram", "Virudhunagar"],
          "Telangana": ["Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal", 
                        "Kamareddy", "Karimnagar", "Khammam", "Komaram Bheem Asifabad", "Mahabubabad", "Mahabubnagar", "Mancherial", 
                        "Medak", "Medchal–Malkajgiri", "Mulugu", "Nagarkurnool", "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad", 
                        "Peddapalli", "Rajanna Sircilla", "Rangareddy", "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy", 
                        "Warangal Rural", "Warangal Urban", "Yadadri Bhuvanagiri"],
          "Tripura": ["Dhalai", "Gomati", "Khowai", "North Tripura", "Sepahijala", "South Tripura", "Unakoti", "West Tripura"],
          "Uttar Pradesh": ["Agra", "Aligarh", "Ambedkar Nagar", "Amethi (Chatrapati Sahuji Mahraj Nagar)", "Amroha (J.P. Nagar)", 
                            "Auraiya", "Ayodhya", "Azamgarh", "Baghpat", "Bahraich", "Ballia", "Balrampur", "Banda", "Barabanki", 
                            "Bareilly", "Basti", "Bhadohi", "Bijnor", "Budaun", "Bulandshahr", "Chandauli", "Chitrakoot", "Deoria", 
                            "Etah", "Etawah", "Farrukhabad", "Fatehpur", "Firozabad", "Gautam Buddha Nagar", "Ghaziabad", "Ghazipur", 
                            "Gonda", "Gorakhpur", "Hamirpur", "Hapur (Panchsheel Nagar)", "Hardoi", "Hathras (Mahamaya Nagar)", 
                            "Jalaun", "Jaunpur", "Jhansi", "Kannauj", "Kanpur Dehat", "Kanpur Nagar", "Kasganj (Kanshiram Nagar)", 
                            "Kaushambi", "Kushinagar (Padrauna)", "Lakhimpur Kheri", "Lalitpur", "Lucknow", "Maharajganj", "Mahoba", 
                            "Mainpuri", "Mathura", "Mau", "Meerut", "Mirzapur", "Moradabad", "Muzaffarnagar", "Pilibhit", "Pratapgarh", 
                            "Prayagraj", "Raebareli", "Rampur", "Saharanpur", "Sambhal (Bhim Nagar)", "Sant Kabir Nagar", "Shahjahanpur", 
                            "Shamli", "Shrawasti", "Siddharthnagar", "Sitapur", "Sonbhadra", "Sultanpur", "Unnao", "Varanasi"],
          "Uttarakhand": ["Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun", "Haridwar", "Nainital", "Pauri Garhwal", 
                          "Pithoragarh", "Rudraprayag", "Tehri Garhwal", "Udham Singh Nagar", "Uttarkashi"],
          "West Bengal": ["Alipurduar", "Bankura", "Birbhum", "Cooch Behar", "Dakshin Dinajpur (South Dinajpur)", "Darjeeling", 
                          "Hooghly", "Howrah", "Jalpaiguri", "Jhargram", "Kalimpong", "Kolkata", "Malda", "Murshidabad", "Nadia", 
                          "North 24 Parganas", "Paschim Medinipur (West Medinipur)", "Purba Medinipur (East Medinipur)", "Purulia", 
                          "South 24 Parganas", "Uttar Dinajpur (North Dinajpur)"],
          "Andaman and Nicobar Islands": ["Nicobar", "North and Middle Andaman", "South Andaman"],
          "Chandigarh": ["Chandigarh"],
          "Dadra and Nagar Haveli and Daman and Diu": ["Dadra and Nagar Haveli", "Daman", "Diu"],
          "Lakshadweep": ["Agatti", "Amini", "Andrott", "Bitra", "Chetlat", "Kadmat", "Kalpeni", "Kavaratti", "Kiltan", "Minicoy"],
          "Delhi": ["Central Delhi", "East Delhi", "New Delhi", "North Delhi", "North East Delhi", "North West Delhi", "Shahdara", 
                    "South Delhi", "South East Delhi", "South West Delhi", "West Delhi"],
          "Puducherry": ["Karaikal", "Mahe", "Puducherry", "Yanam"]
      }

    # for state in states:
    #   models.States.objects.create(state_name=state)
    state = models.States.objects.all()
    district = models.Districts.objects.all()

    # return render(request, 'pages/index.html')
    #return render(request, 'accounts/sign-in.html')
    message = ""
    msg_alert = False
    duplicate_checking = request.session.get('duplicate_check')
    if duplicate_checking:
      message = "The entered phone number has already used"
      msg_alert = True
      request.session['duplicate_check'] = False

    if request.method == 'POST':
        ip = get_client_ip(request)
        print("ip", ip)
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        company = request.POST.get('company')
        type = request.POST.get('type')
        state = request.POST.get('state')
        district = request.POST.get('district')
        medium = request.POST.get('medium')
        # print("comp: ", company)
        # print("type: ",type)
        # print("state: ", state)
        # print("dist: ", district)
        if models.User.objects.filter(phone_number=phone).exists():
          request.session['duplicate_check'] = True
          return redirect('index')
        else:
        # print("home name : ", user.name)
        # print("home phone : ", user.phone_number)
        # print("home Id: ", user.id)
          user = models.User.objects.create(name=name, phone_number=phone, start_time=datetime.now(), 
                                            company = company, type = type, district = district, state = state, ip_address = ip , medium = medium)
          request.session['User ID'] = user.id
          request.session['medium'] = user.medium
          request.session['User Name'] = user.name
          request.session['User Phone'] = user.phone_number
          # request.session['participant company'] = user.company
          # request.session['participant type'] = user.type
          # request.session['participant district'] = user.district
          # request.session['participant state'] = user.state
          # Optionally, you can log to a file
          # with open('log.txt', 'a') as f:
          #     f.write(f"Name: {name}, Phone: {phone}\n")

          # Return a JSON response (optional)
          # request.session.pop('shuffled_questions', None) # delete session
          return redirect('quiz_page')

    # Render the initial form if GET request
    return render(request, 'pages/quiz_home.html', {
                  'msg_alert': msg_alert,
                  'error_message': message, 'states': states,
                  'districts': districts, 'bg_image': bg_image_url,
              })
  except Exception as e:
    return redirect('index')

def quiz_page(request):
  try:
    user_id = request.session.get('User ID', 0)
    user_name = request.session.get('User Name', "")
    user_phone = request.session.get('User Phone', 0)
    medium = request.session.get('medium', "")
    print('medium :' , medium )
    if user_id == 0:
      return redirect('index')
    bg_image = models.BgImage.objects.filter(type = 'Background').first()
    bg_image_url =  bg_image.image if bg_image else None
    # bg_image = models.BgImage.objects.filter(type = 'Background').first()
    if 'shuffled_questions' not in request.session:
      all_questions = list(models.Questions.objects.filter(if_view =True , medium = medium))
      print(all_questions)
      random.shuffle(all_questions)
      request.session['shuffled_questions'] = [question.pk for question in all_questions]
      request.session['current_question_index'] = 0
      request.session['sequence_number'] = 1

    shuffled_questions = request.session['shuffled_questions']
    current_question_index = request.session['current_question_index']
    sequence_number = request.session['sequence_number']

    if current_question_index >= len(shuffled_questions):
        return redirect('quiz_results')  # No more questions, go to the results page

    current_question_id = shuffled_questions[current_question_index]
    question = models.Questions.objects.get(pk=current_question_id)
    print(question)
    choices = question.choices.all()

    if request.method == 'POST':
        # user_obj = models.User.objects.get(id=user_id)
        # user_obj = models.User.objects.first()
        ip = get_client_ip(request)
        # user_id = user_obj.id#request.session.get('User ID')
        # users_name = user_obj.name # request.session.get('participant Name')
        # users_phone = user_obj.phone_number #request.session.get('participant Phone number')
        # users_company = user_obj.company #request.session.get('participant company')
        # users_type = user_obj.type #request.session.get('participant type')
        # users_district = user_obj.district #request.session.get('participant district')
        # users_state = user_obj.state #request.session.get('participant state')
        #

        selected_choice_id = request.POST.get('choice')
        if selected_choice_id is None:
              selected_choice = models.Choices.objects.get(choice="no choice selected")
        else:
              selected_choice = models.Choices.objects.get(pk=selected_choice_id)
              # print(selected_choice)

        correct_choice = question.choices.filter(is_answer=True).first()


        models.QuizzExam.objects.create(
            # user=user_obj, user_name=user_obj.name, user_phone=user_obj.phone_number,
            user_name= user_name, user_phone=user_phone,
            question_id=question.id, question_name=question.question,
            selected_choice=selected_choice.choice, correct_choice=correct_choice.choice,
            is_answer_correct=(selected_choice == correct_choice), choice_selected_time=datetime.now()
        )

        request.session['current_question_index'] += 1
        request.session['sequence_number'] += 1

        if request.session['current_question_index'] >= len(shuffled_questions):
            # user_obj = models.User.objects.first()
            user_obj = models.User.objects.get(id=user_id)
            exam_start_time = user_obj.start_time.replace(tzinfo=None)  # Convert to naive datetime
            end_time = datetime.now().replace(tzinfo=None)

            answers_count = models.QuizzExam.objects.filter(user_phone=user_obj.phone_number).count()
            correct_answers_count = models.QuizzExam.objects.filter(user_phone=user_obj.phone_number, is_answer_correct=True).count()
            wrong_answers_count = models.QuizzExam.objects.filter(user_phone=user_obj.phone_number, is_answer_correct=False).count()
            duration_in_minutes = (end_time - exam_start_time).total_seconds()
            total_questions_count = models.Questions.objects.count()
            percent = (correct_answers_count * 100) / total_questions_count
            models.Results.objects.create(
                user=user_obj, user_name=user_obj.name, ip_address = ip, user_phone=user_obj.phone_number, user_company = user_obj.company,
                user_type = user_obj.type, user_district = user_obj.district, user_state = user_obj.state, no_of_questions_attended = answers_count,
                exam_start_datetime=exam_start_time, exam_end_datetime=end_time, duration=duration_in_minutes, 
                correct_answers=correct_answers_count, wrong_answers=wrong_answers_count, percentage=percent)
            return redirect('quiz_results')  # Redirect to the results page

        return redirect('quiz_page')  # Redirect to the same page to load the next question

    # Render the template with the current question and its choices
    return render(request, 'pages/quiz_data.html', {'bg_image': bg_image_url if bg_image else None, 
                                                    'question': question, 'choices': choices, 'sequence_number': sequence_number})
  except Exception as e:
    return redirect('index')
  
def quiz_page2(request):
  return render(request, 'pages/quiz_data2.html')

def quiz_results(request):
    user_id = request.session.get('User ID', 0)
    if user_id == 0:
      return redirect('index')
    
    request.session.flush()  # Clear the session data
    # Logic to calculate and display results
    return render(request, 'pages/quiz_results.html')

# Sections
def presentation(request):
  return render(request, 'sections/presentation.html')

def page_header(request):
  return render(request, 'sections/page-sections/hero-sections.html')

def features(request):
  return render(request, 'sections/page-sections/features.html')

def navbars(request):
  return render(request, 'sections/navigation/navbars.html')

def nav_tabs(request):
  return render(request, 'sections/navigation/nav-tabs.html')

def pagination(request):
  return render(request, 'sections/navigation/pagination.html')

def forms(request):
  return render(request, 'sections/input-areas/forms.html')

def inputs(request):
  return render(request, 'sections/input-areas/inputs.html')

def avatars(request):
  return render(request, 'sections/elements/avatars.html')

def badges(request):
  return render(request, 'sections/elements/badges.html')

def breadcrumbs(request):
  return render(request, 'sections/elements/breadcrumbs.html')

def buttons(request):
  return render(request, 'sections/elements/buttons.html')

def dropdowns(request):
  return render(request, 'sections/elements/dropdowns.html')

def progress_bars(request):
  return render(request, 'sections/elements/progress-bars.html')

def toggles(request):
  return render(request, 'sections/elements/toggles.html')

def typography(request):
  return render(request, 'sections/elements/typography.html')

def alerts(request):
  return render(request, 'sections/attention-catchers/alerts.html')

def modals(request):
  return render(request, 'sections/attention-catchers/modals.html')

def tooltips(request):
  return render(request, 'sections/attention-catchers/tooltips-popovers.html')