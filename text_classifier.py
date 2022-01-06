import re
import processing_data as proc
import utils
import warnings
warnings.filterwarnings("ignore")


l_tfidf = utils.load_pickle_file("tfidf.pickle")
l_svm_model = utils.load_pickle_file("svm.pickle")
l_label_encoder = utils.load_pickle_file("encoder.pickle")


list_appreciation_keywords = ["اشكركم", "الشكر", "التقدير", "ممتازة", "رائع", "لطيفة", "لطيف", "رضا", "ممتاز", "رائعين",
                              "رائعون", "amazing", "professional", "kind", "helpful", "great", "حفاوة الاستقبال",
                              "حفاوة", "مرة شكرا", "غير مادي", "شكر"]

list_complain_keywords = ["اشتكي", "يشتكي", "اشتكيت", "متسخة", "سيء", "غيرمقبول", "شكوى", "اشكو", "very bad", "أسوأ ",
                          "تكاليف مرتفعة", "تكالف علية", "مبالغ مرتفعة", "مبالغ عالية", "يتعجرف", "متعجرف", "بتعجرف",
                          "تعجرف", " قديم ", "عفن", "معفن", "العيب", "عيب", "حرام", "فاشل", "أسوأ", "اسوأ",
                          "أسوى ", "أسوء",
                          "poor", "rude", "arrogant", "لايرتقي", "لا يرتقي", "لا يناسب", "للأسف", "للإسف", "للاسف ",
                          "عليهم ملاحظات", "حسبنا الله", "حسبي", "حسبنا", "لايحترم", "الاسف",
                          "خطأ", "خطاء", "ليست انسانيه",
                          "سيئة", "وإنفعالية", "تكلفة عالية", "بتكلفة عالية"
                                                              "لم يحترم", "لا يحترم", "لا يوجد احترام", "اسواء",
                          "متدني", "اسلوب حاد", "أسلوب حاد",
                          "سي جدا",
                          "كذب", "كاذب", "كذاب", "مغرور", "مضره", "مضرة", "مضر", "ماديين", "التعامل مادي", "نفسيات",
                          "قديم جدا", "لا يليق", "باستثناء", "مخيف", "كابوس", "السوء", "اساءه", "لايتمتع", "حسبي الله",
                          "اعوذ بالله", "not good", "Not", "not", "لا يعمل", "لا يعمل", "وقح", "زباله",
                          "وغير محترم", "زفت", "ما يوصل", "مايوصل", "متغطرس", "استفزني", "قاسي", " يكره", " اكره ",
                          " يكرهك ", "لا يريد", "except", "لاتفقه", "لا تفقه", "يفتقدون", "قلة ادب", "تالف", "تالفة",
                          "تالفه", "لم تعاملنا", "لااتعامل", "لن اتعامل", "لا يمت", "خصوصية", "خصوصيات", "too long",
                          "عنصري", "عنصرية", "يتعنصر", "عصبي", "يعصب", "لا يهتم", "طردني", "طردتني", "كبرياء", "متكبر",
                          "الكبرياء", "should respect", "lazy", "not active", "لن أعود", "مايفهم", "ما يفهم", "مايعرف",
                          "ما يعرف", "lack", "لا يعطي", "but", "But", "Unable", "unable", "horrible", "bad",
                          "اتقو الله", "اتقوا االله", "محرم", "قليلة أدب", "قليلة ادب", "ضحك", "يبكي", "ماتعطي",
                          " ما تعطي", " يؤلم ", " ألم ", " الم ", " مؤلم ", " موجع ", " يوجع ", " فظ ", "مادي",
                          " ماديين", " مادية ", "يلعن", "يلعنه", "يلعنهم", "يلعنها", "مؤسف", "مؤسفة", "مجرم", "مجرمة",
                          "ما حبيت", "ماحبيت", "ملاحظة", "نحتاج", "يحتاج", "تحتاج", "اقتراح",
                          "التوضيح", "يا ليت", "ملاحظ", "الملاحظ", "لا يستحق", "مجزرة",
                          "استعجال", "تعالي", "تكبر", "قلة احترام", "قلة", "تشكو", "مخيب", "لا يساعد", "لايساعد", "طفش",
                          "سئي", "لا تعمل", "اسوء", "للاسوء", "لايستحق", "لا يحترم", "unprofessional",
                          "لم يكن", "تأخر", "اقل المستوى", "أقل المستوى", "اقل مستوى", "ماتعرف", "مايعرف", "مايدري",
                          "ماتدري", "بدون جدية", "جاف", "لا تعمل", "لاتعمل", "لا يعمل", "لا يعمل", "ولاتعطي", "لايعطي",
                          "لا انصح", "يفقدون حسن", "يفتقدون لحسن", "يفقدون حسن", "لايهمه", "لا يهمه", "لكن", "بطيء",
                          "بطيئين", "بطيئ", "بطء", "استفزاز", "إستفزاز", "تأخير", "but", "But", "لا تعطي", "لا يعطي",
                          "سئ ", "سيئ", "سيئه", "لن اعود", "لن أعود", "لن تتكرر", "لن اكرر"
                                                                                  "لا يتقيد", "لا يتقيدن", "لا يلتزم",
                          "tugh", "tough", "aggressive", "متبلد", "متجل", "مستعجل", "لا يشرح",
                          "لايشرح", "شكواه", "عانيت", "معاناة", "توتر", "يوتر", "كثير الكلام", "كثيرات الكلام",
                          "كثيرات الحديث", "كثير الحديث", "stress", "couldn't", "couldnt", "صوت عالي", "صوت مرتفع",
                          "لا زلت مريض",
                          "ينقص", "Worst", "worst", "no cooperation", "worst", "too slow", "slow", "SLOW", "Slow"
                                                                                                           "Bad",
                          "nervous", "تنبيه", "تنبية",
                          "disaster", "مزعج", "غلظة", "جفوة", "negative", "Negative", "RUDE", "STUPID", "Stupid",
                          "stupid", "glitches", "without informing", "weak", "Weak", "لايرقى", "لايقوم", " سؤ ",
                          "دون المستوى", "needs to respect", "need to respect", "Miss ", "miss", "تكدس", "لايخدم",
                          "لا يخدم", "فوضى", "لازلت مريض", "لازلت", "معدوم", "لا يملكون", "لايملكون", "لم يعطي",
                          "انحدار", "انحدر", "إنحدار", "إنحدر", "تدني", "متدني", "اموت", "متململ", "ممنوع", "لا أنصح",
                          "لاانصح", "لاأنصح", "لا انصح", "ما أنصح", "ماانصح", "ماأنصح", "ما انصح", "تحطيم", "لاتتقن",
                          "لا تتقن", "لا يتقن", "لايتقن", "احقر", "حقير", "ازعاج ", "مزعج", " مخيب ", " خيب ",
                          "irritating", "alarming", "احتقار", "مؤذي", "inexperienced", "misbehave", "سيّء", "متعطل ",
                          "dont do to provide any help", "inappropriate", "disappointed", "loudly", "عدم تقيد",
                          "scare", "بلا سبب", "دون سبب", "غير مهيء", "غير مهيئ", "must learn", "عندي مشاكل",
                          "عندي مشكلة",
                          "عنا مشكلة", "عنا مشاكل", "اواجه مشكلة", "اواجه مشاكل", "في مشاكل", "problem", "Problem",
                          "أواجه مشكلة", "أواجه مشاكل", "unpleasant", "I don’t recommend", "دونية", "دونيه", "خسيس",
                          "arrogance", "يؤسف", "يفتفد", "no respect", " أكره ", "هابط", "worest", "worst", "shocked",
                          "ما كان كويس", "ما كانت كويسة", "ما كانت كويسه", "غير متفهم", "غير متعاون", "بطئ", "دخان",
                          "يدخن ", "بدخن ",
                          "شايف حاله", "شايفة حالها ", "شايف نفسه ", "شايفة نفسها ", "لا تتجاوب", "لاتتجاوب"
                          ]

list_wishing_words = ["الرجاء", "رجاء", "نتمنى", "اتمنى", "أتمنى", "نرجو", "أرجو", "ترغب", "نرغب", "أود", "يرغب"]


def get_chunk_text(text, num_words=12):
    list_chunks = []
    mini_text = ""
    for word in text.split():
        mini_text += word + " "
        if len(mini_text.split()) >= num_words:
            list_chunks.append(mini_text)
            mini_text = ""
    list_chunks.append(mini_text)
    return list_chunks


def predict_label(list_texts):
    c_complaint = 0
    c_appreciation = 0

    if len(list_texts) >= 2:
        if len(list_texts[-1].split()) < 5:
            list_texts[-2] = list_texts[-2] + list_texts[-1]
            list_texts.pop()

    for text in list_texts:

        sample_test_tfidf = l_tfidf.transform([text])
        if len(sample_test_tfidf.data) == 0:
            flag_complaint_label = False
            for complaint_word in list_complain_keywords:
                if re.search(complaint_word, text):
                    flag_complaint_label = True

            if flag_complaint_label:
                c_complaint += 1
            else:
                c_appreciation += 1

        predicted_label = l_label_encoder.classes_[l_svm_model.predict(sample_test_tfidf)][0]
        if predicted_label == 'Complaint':
            if text.strip() in ["لا يوجد", "لايوجد", "لايوجد ملاحظات", "لا يوجد ملاحظات", "لا يوجد اي ملاحظات",
                                "لا يوجد أي ملاحظات"]:
                c_appreciation += 1
            else:
                c_complaint += 1
        elif predicted_label == 'Appreciation':
            flag_exist_complaint = False
            for complaint_word in list_complain_keywords:
                if re.search(complaint_word, text):
                    if complaint_word in list_wishing_words and predicted_label == 'Appreciation':
                        flag_exist_complaint = False
                    else:
                        flag_exist_complaint = True
                        c_complaint += 1

            if not flag_exist_complaint:
                c_appreciation += 1

    ratio_complaint = round(c_complaint / (c_complaint + c_appreciation), 2)
    ratio_appreciation = round(c_appreciation / (c_appreciation + c_complaint), 2)
    if ratio_appreciation > ratio_complaint == 0.0:
        return ["Appreciation", ratio_appreciation]
    else:
        return ["Complaint", ratio_complaint]


def remove_common_words(text):
    list_common_words = ["دكتور", "ممرض", "طبيب", "اطباء", "أطباء", "مستشفى", "صيدلي", "عيادة", "موعد", "اجراء",
                         "إجراء",
                         "ادارة", "إدارة", "اطفال", "أطفال"]
    returned_text = text
    for word in text.split():
        for c_word in list_common_words:
            if re.search(c_word, word):
                returned_text = returned_text.replace(word, " ")

    return " ".join(returned_text.split()).strip()


def clean_text1(text):
    clean_text = proc.clean_text(text=text)
    clean_common_words = remove_common_words(text=clean_text)
    clean_stop_words = proc.remove_stop_words(text=clean_common_words)

    return clean_stop_words


def prediction(text):
    try:
        clean_text = clean_text1(text=text)
        if clean_text is None:
            return ["Unknown", 1.0]
        list_texts = get_chunk_text(text=clean_text)

        return predict_label(list_texts)

    except Exception as e:
        print(e)
        return ["Unknown", 1.0]


# test_text = """ كل الخدمات كانت جيدة وممتازة وشكرا لجميع العاملين لكن يوجد ممرض سيء التعامل ومزعج  """
# print(prediction(text=test_text))
