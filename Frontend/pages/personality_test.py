import streamlit as st
import requests
import math

API_URL = "http://127.0.0.1:8000"

def get_question(API_URL):
    """Pobiera listę pytań (tytuły i ID) z API."""
    question_url = f"{API_URL}/get_all_questions_id"
    response = requests.get(question_url)
    if response.status_code == 200:
        return response.json()['Questions']
    else:
        st.warning("Coś poszło nie tak przy pobieraniu pytań.")
        return []

def get_answers(API_URL,question_id):
    """Pobiera możliwe odpowiedzi (A/B) dla danego pytania."""
    answer_url = f"{API_URL}/answer_by_question/{question_id}/"
    response = requests.get(answer_url)
    if response.status_code == 200:
        return response.json()['Answers']
    else:
        st.warning("Coś poszło nie tak przy pobieraniu odpowiedzi.")
        return []
    
def get_personality(API_URL,personality_symbol):
    """Pobiera osobowość na podstawie kodu """
    answer_url = f"{API_URL}/get_personality/{personality_symbol}/"
    response = requests.get(answer_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.warning("Coś poszło nie tak przy pobieraniu osobowości.")
        return {}
    
def post_form(API_URL, answers, name, id):
    new_form = {
        'Answers': answers,
        'UserName': name,
        'PersonalitiesId':id
    }
    form_url = f"{API_URL}/form/"
    response = requests.post(form_url, json=new_form)

    if response.status_code == 200:
        # print("Sukces! Odpowiedź z serwera:")
        # print(response.json())  # Jeśli odpowiedź jest w formacie JSON
        response.json()
    else:
        print(f"Błąd! Status code: {response.status_code}")
        print(response.text)  # Szczegóły odpowiedzi tekstowej

    

def reset_quiz():
    """Resetuje stan quizu i przeładowuje aplikację."""
    for key in list(st.session_state.keys()):
        if key.startswith("session_"):
            del st.session_state[key]
    st.session_state.game_started = False
    st.session_state.current_session = 0
    st.session_state.session_answers = []
    st.session_state.all_confirmed = False
    st.session_state.name = ""
    # st.rerun()

def confirm_session():
    """
    Zatwierdza odpowiedzi z bieżącej sesji i zapisuje je do session_answers.
    Jeśli nie jest to ostatnia sesja, przechodzi do kolejnej.
    Jeśli to była ostatnia sesja, ustawia all_confirmed = True -> przejście do podsumowania.
    """
    current_sess = st.session_state.current_session
    session_qna = []

    # Zbieramy odpowiedzi z aktualnie wyświetlanej sesji
    for q_id in st.session_state.session_question_ids:
        user_choice = st.session_state.get(f"session_{current_sess}_question_{q_id}", None)
        session_qna.append(user_choice)
    
    st.session_state.session_answers.append(session_qna)

    total_sessions = st.session_state.total_sessions
    # Jeśli to nie była ostatnia sesja -> przechodzimy do kolejnej
    if current_sess < total_sessions - 1:
        st.session_state.current_session += 1
    else:
        # Ostatnia sesja -> do podsumowania
        st.session_state.all_confirmed = True

    # st.rerun()

def count_answers():
    # Spłaszczamy wszystkie odpowiedzi
    all_answers_flat = [
        ans for session_ans in st.session_state.session_answers for ans in session_ans
    ]


    return "".join(all_answers_flat)

def check_features(answers):
    features = {'E':0, 
                'I':0, 
                'S':0, 
                'N':0, 
                'T':0, 
                'F':0, 
                'J':0,
                'P':0 }
    for element in answers:
        if element in features:
            features[element] += 1

    return features

def check_personality_symbol(counted_answers):
    personality_symbol = ""
     
    if counted_answers['E'] > counted_answers['I']:
        personality_symbol += 'E'
    else:
        personality_symbol += 'I'
    
    if counted_answers['S'] > counted_answers['N']:
        personality_symbol += 'S'
    else:
        personality_symbol += 'N'

    if counted_answers['T'] > counted_answers['F']:
        personality_symbol += 'T'
    else:
        personality_symbol += 'F'

    if counted_answers['J'] > counted_answers['P']:
        personality_symbol += 'J'
    else:
        personality_symbol += 'P'

    return personality_symbol

def final_page(questions):

    # *** PODSUMOWANIE – gdy all_confirmed = True ***
    
    if st.session_state.name:
        st.write(f"Dziękujemy {st.session_state.name} za wypełnienie pytań!")
        name = st.session_state.name
    else:
        st.write("Dziękujemy za wypełnienie pytań!")
        name = ''

    answers = count_answers()
    features = check_features(answers)
    symbol = check_personality_symbol(features)
    personality = get_personality(API_URL,symbol)


    st.write(f"Twoja osobowość to: {personality['Name']}")
    st.write(f"Kod osobowości to: {personality['Symbol']}")
    st.write(f"Chcesz dowiedzieć się wiecej o swojej osobowości, wejdz na:")
    st.write(f"{personality['Content']}")

    post_form(API_URL, answers, name, personality['PersonalitiesId'])


    # Możliwość powtórzenia quizu
    st.button("Powtórz quiz", on_click=reset_quiz)

def test():
    # -- Inicjalizacja stanów --
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    
    if "current_session" not in st.session_state:
        st.session_state.current_session = 0

    if "session_answers" not in st.session_state:
        st.session_state.session_answers = []

    if "all_confirmed" not in st.session_state:
        st.session_state.all_confirmed = False

    if "name" not in st.session_state:
        st.session_state.name = ""

    # Pobranie wszystkich pytań
    questions = get_question(API_URL)
    if not questions:
        st.write("Brak pytań do wyświetlenia.")
        return

    # Obliczamy liczbę "zestawów" (sesji) – po 5 pytań w jednej sesji
    questions_per_session = 5
    total_questions = len(questions)
    total_sessions = math.ceil(total_questions / questions_per_session)
    st.session_state.total_sessions = total_sessions

    # -- EKRAN POWITALNY --
    if not st.session_state.game_started:
        st.title("Witamy w quizie A/B!")
        st.write("Kliknij przycisk, aby rozpocząć grę.")
        if st.button("Rozpocznij grę"):
            st.session_state.game_started = True
            st.rerun()
        return

    # -- WYŚWIETLANIE PYTAŃ (sesjami) / OSTATECZNE PODSUMOWANIE --
    if not st.session_state.all_confirmed:
        # *** JESTEŚMY W TRYBIE WYŚWIETLANIA PYTAŃ ***
        current_sess = st.session_state.current_session
        st.title(f"Odpowiedz na zestaw pytań {current_sess + 1}")

        # Określamy, które pytania należą do aktualnego zestawu
        start_idx = current_sess * questions_per_session
        end_idx = start_idx + questions_per_session
        session_questions = questions[start_idx:end_idx]

        # Pamiętamy ID pytań z bieżącej sesji, by móc je sczytać podczas zatwierdzania
        st.session_state.session_question_ids = [q["QuestionId"] for q in session_questions]

        # Wyświetlamy pytania
        for question in session_questions:
            q_id = question["QuestionId"]
            answers = get_answers(API_URL, q_id)
            if len(answers) < 2:
                st.warning(f"Nieprawidłowa liczba odpowiedzi dla pytania ID={q_id}")
                continue

            labels = [answers[0]["Content"], answers[1]["Content"]]
            marks = [answers[0]["MarkSign"], answers[1]["MarkSign"]]

            # Radio niezaznaczone początkowo (index=-1)
            st.radio(
                label=question["Content"],
                options=marks,
                key=f"session_{current_sess}_question_{q_id}",
                index=None,
                format_func=lambda mark: labels[marks.index(mark)]
            )

        # Sprawdzamy, czy użytkownik zaznaczył wszystkie pytania z bieżącego zestawu
        answered_all = True
        for q_id in st.session_state.session_question_ids:
            if st.session_state.get(f"session_{current_sess}_question_{q_id}", None) is None:
                answered_all = False
                break

        # Jeżeli wszystkie zaznaczone
        if answered_all:
            # Jeśli nie jest to ostatnia sesja -> tylko przycisk „Zatwierdź zestaw pytań”
            if current_sess < total_sessions - 1:
                st.button("Zatwierdź zestaw pytań", on_click=confirm_session)
            else:
                # OSTATNI zestaw – pokazujemy pole na imię oraz przycisk „Zatwierdź quiz”
                st.text_input("Podaj swoje imię (opcjonalnie)", key="name")
                st.button("Zatwierdź quiz", on_click=confirm_session)
        else:
            st.write("Odpowiedz na wszystkie pytania, aby móc zatwierdzić ten zestaw.")
    else:
        final_page(questions)

test()
