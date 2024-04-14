import random
import os
import argparse
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import sys
from infinite_stream import main

questions_to_file_map = {
    "And what part of the job description caught your attention first?":"And_what_part_of_the_job_description_caught_your_attention_first_",
    "Hello, how are you doing today?":"Hello!_How_are_you_doing_today_",
    "But do you think it's easy to find that kind of opportunity as a fresher? ":"But_do_you_think_it_is_easy_to_find_that_kind_of_opportunity_as_a_fresher_",
    "But what about freshers who just graduated? What are your suggestions for them?":"But_what_about_freshers_who_just_graduated__What_are_your_suggestions_for_them_",
    "Can you describe what you worked on in finance?":"Can_you_describe_what_you_worked_on_in_finance_",
    "Can you describe what you worked on in marketing?":"Can_you_describe_what_you_worked_on_in_marketing_",
    "Can you describe what you worked on in the healthcare department?":"Can_you_describe_what_you_worked_on_in_the_healthcare_department_",
    "Can you tell me why you want this job in the first place?":"Can_you_tell_me_why_you_want_this_job_in_the_first_place_",
    "Don't worry, it is just a formality. Shall we begin? The first interview, for the technical position, will start when you say: I am ready to start the technical interview":"Do_not_worry,_it_is_just_a_formality._Shall_we_begin_",
    "Do you prefer working on your own or with a team?":"Do_you_prefer_working_on_your_own_or_with_a_team_",
    "Explain an instance where you were forced to make a challenging decision based with limited  knowledge. What was the next step you took?":"Explain_an_instance_where_you_were_forced_to_make_a_challenging_decision_based_with_limited_knowledge",
    "Oh, that's fantastic then let's begin, shall we? The first interview, for the technical position, will start when you say: I am ready to start the technical interview":"Fantastic._Shall_we_begin_",
    "Glad to hear that. So, are you nervous?":"Glad_to_hear_that._Are_you_nervous_about_the_interview_",
    "Goodbye, take care!":"Goodbye,_take_care!",
    "Hello, how are you doing today?":"Hello!_How_are_you_doing_today_",
    "How did you hear about this offer?":"How_did_you_hear_about_this_offer_",
    "Imagine a situation where you are asked to submit a report as a team and everybody has a different mindset about how the project should work, how would you get everyone on the same page?"
    :"Imagine_a_situation_where_you_are_asked_to_submit_a_report_team",
    "In a work life culture, what do you think is more important to have: qualification or experience?":"In_a_work_life_culture,_what_do_you_think_is_more_important_to_have__qualification_or_experience_",
    "In what manner would you inform a client of terrible news?":"In_what_manner_would_you_inform_a_client_of_terrible_news_",
    "Let's say you are given contradicting information. In order to get reliable conclusions, how would you resolve the disparities to reach trustworthy conclusions?":"Let_us_say_you_are_given_contradicting_information",
    "Is it because you’re nervous about the interview?":"Sorry_to_hear_that._Are_you_nervous_about_the_interview_",
    "Sounds interesting  but do you think it would be realistic to expect that?":"Sounds_interesting_but_do_you_think_it_would_be_realistic_to_expect_that_",
    "Thank you for your answers. Are you ready for the financial interview?":"Thank_you_for_your_answers._Are_you_ready_for_the_financial_interview_",
    "Thank you for your answers. Are you ready for the last interview, the medical one?":"Thank_you_for_your_answers._Are_you_ready_for_the_last_interview,_the_medical_one_",
    "Thank you for your answers. Are you ready for the marketing interview?":"Thank_you_for_your_answers._Are_you_ready_for_the_marketing_interview_",
    "That’s great, as you should be aware,  this job is for people with technical background.":"That_is_great,_as_you_should_be_aware,_this_job_is_for_people_with_a_technical_background.",
    "This was the last interview, thank you for your cooperation!":"This_was_the_last_interview,_thank_you_for_your_cooperation!",
    "To know more about your technical background, can you describe a project you have done related to IT? ":"To_know_more_about_your_technical_background,_can_you_describe_a_project_you_have_done_related_to_IT_",
    "What are your qualifications and how do they add weightage to your work?":"What_are_your_qualifications_and_how_do_they_add_weightage_to_your_work_",
    "What exactly does work life balance mean to you?":"What_exactly_does_work_life_balance_mean_to_you_",
    "When solving a problem, how do you confirm that your assumptions or hypotheses are correct?":"When_solving_a_problem,_how_do_you_confirm_that_your_assumptions_or_hypotheses_are_correct_",
}

technical_questions = [
    "Hello, how are you doing today?",
    "Glad to hear that. So, are you nervous?",
    "Don't worry, it is just a formality. Shall we begin? The first interview, for the technical position, will start when you say: I am ready to start the technical interview",
    "In a work life culture, what do you think is more important to have: qualification or experience?",
    "But what about freshers who just graduated? What are your suggestions for them?",
    "But do you think it's easy to find that kind of opportunity as a fresher? ",
    "Explain an instance where you were forced to make a challenging decision based with limited  knowledge. What was the next step you took?",
    "To know more about your technical background, can you describe a project you have done related to IT? ",
    "What are your qualifications and how do they add weightage to your work?",
    "Thank you for your answers. Are you ready for the marketing interview?"
]

marketing_questions = [
    "Can you tell me why you want this job in the first place?",
    "And what part of the job description caught your attention first?",
    "Let's say you are given contradicting information. In order to get reliable conclusions, how would you resolve the disparities to reach trustworthy conclusions?",
    "Can you describe what you worked on in marketing?",
    "What are your qualifications and how do they add weightage to your work?",
    "Thank you for your answers. Are you ready for the financial interview?"
]

financial_questions = [
    "Imagine a situation where you are asked to submit a report as a team and everybody has a different mindset about how the project should work, how would you get everyone on the same page?",
    "When solving a problem, how do you confirm that your assumptions or hypotheses are correct?",
    "Can you describe what you worked on in finance?",
    "What are your qualifications and how do they add weightage to your work?",
    "Thank you for your answers. Are you ready for the last interview, the medical one?"
]

healthcare_questions = [
    "What exactly does work life balance mean to you?",
    "Sounds interesting  but do you think it would be realistic to expect that?",
    "In what manner would you inform a client of terrible news?",
    "Can you describe what you worked on in the healthcare department?",
    "What are your qualifications and how do they add weightage to your work?",
    "This was the last interview, thank you for your cooperation!",
    "Goodbye, take care!"
]

questions = {
    "technical": technical_questions,
    "marketing": marketing_questions,
    "financial": financial_questions,
    "healthcare": healthcare_questions
}

def pr(arg):
    sys.stdout.write(f'{arg}"\n"')
    sys.stdout.flush()

def retrieve_sentence(voice_name, sentence):
    file_path = os.path.join('voices\\', voice_name, questions_to_file_map[sentence] + '.wav')
    pr(file_path)
    if not os.path.exists(file_path):
        pr("do not exist")
        return None
    with open(file_path, 'rb') as file:
        audio_data = file.read()
        audio_segment = AudioSegment.from_wav(BytesIO(audio_data))
        play(audio_segment)
    return audio_data

def generate_voice_order():
    voices_name = ["william","megan","pixie","robot"]
    random.shuffle(voices_name)
    return voices_name

def microphone(question, participant= None):
    speech_live = main()
    pr(f'Speech Content: {speech_live}')
    with open("last_answer.txt", 'w') as file:
        file.write(speech_live)
    with open(f'{participant}-full_script.txt', 'a') as file:
        file.write(question)
        file.write("\n")
        final_sentence = speech_live + "\n\n"
        file.write(final_sentence)
        

def play_audio_and_run_code(questions, participant = None):
    voice_list = generate_voice_order()
    with open(f'{participant}-full_script.txt', 'w') as file:
        for voice in voice_list : 
            file.write(voice)
            file.write(" ")
        file.write("\n")

    for voice in voice_list:
        with open(f'{participant}-full_script.txt', 'a') as file:
            file.write('-------\n')
            file.write(voice)
            file.write("\n")
            file.write('-------\n')
        for key, value in questions.items():
            for question in value:
                retrieve_sentence(voice, question)
                microphone(question, participant)
            pr(f'End of {key} Interview')
        pr(f'End of interview with {voice}')
    pr(f'End of interview')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--participant',type=str,help='Participant Name')

    args = parser.parse_args()

    if args.participant:
        name = args.participant
        pr('Press Enter when the speaker is done to move to the next question')
        play_audio_and_run_code(questions,name)
    else:
        print('You must provide Participant Name')
        print('run python main.py -p Participant-Name')
        

