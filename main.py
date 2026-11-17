from gemini import *
from tavily import *

article = generate_first_sentences()

while True:
    article_title = article['article']['title']
    article_text = article['article']['text']
    article_translation = article['article']['translation']

    print(f"\n{'=' * 60}")
    print(f"오늘의 영어 기사: {article_title}")
    print(f"{'=' * 60}\n")
    print(article_text)

    reading_session = {
        "title": article_title,
        "text": article_text,
        "question_answers": [],
        "follow_up_history": []
    }

    for q in article['question']:
        article_question = q['text']

        print(f"\n[독해 문제]\n{article_question}\n")

        user_answer = input("나의 답변: ")

        reading_session["question_answers"].append({
            "question": article_question,
            "answer": user_answer
        })

        reading_session["follow_up_history"].append([])

    reading_session = evaluate_answers(reading_session)

    # 맞출 때까지 추가 질문하면서 반복.
    while True:
        pending_questions = []

        for i, status in enumerate(reading_session["status"]):
            if status == "wrong":
                follow_up = reading_session["follow_up_question"][i]

                if follow_up:
                    pending_questions.append(i)

        if len(pending_questions) == 0:
            break

        for i in pending_questions:
            follow_up = reading_session["follow_up_question"][i]

            print(f"\n[문제 {i + 1} - 추가 질문]")
            print(f"AI의 질문: {follow_up}\n")

            user_answer = input("나의 답변: ")

            reading_session["follow_up_history"][i].append({
                "question": follow_up,
                "answer": user_answer
            })

        reading_session = evaluate_answers(reading_session)

    # 정답과 tmi 출력.
    print("\n" + "=" * 60)
    print("모든 문제를 해결했습니다!")
    print("=" * 60)

    print("\n[기사 전체 번역]")
    print(article_translation)

    print("\n[문제 및 정답 확인]")
    for q in article['question']:
        print(f"\n문제: {q['text']}")
        print(f"모범 답안: {q['answer']}")

    print("\n" + "=" * 60)
    print("알아두면 좋은 추가 지식")
    print("=" * 60)

    tmis = article['tmi']
    for tmi in tmis:
        print(f"\n[{tmi['title']}]")
        print(tmi['content'])

    # 다음 주제 추천.
    print("\n" + "=" * 60)
    print("다음에 읽어볼 만한 관련 주제")
    print("=" * 60)

    for i, related_topic in enumerate(article['related_topic']):
        print(f"\n[{i + 1}] {related_topic['topic']}")
        print(f"이전 기사와의 연결: {related_topic['connection']}")
        print("-" * 60)

    # 사용자의 다음 주제 선택.
    while True:
        user_selected_related_topic = input(
            "\n다음 기사로 읽고 싶은 주제를 선택하세요.\n"
            "추천 주제의 번호를 입력하거나, 직접 궁금한 주제를 입력할 수 있습니다.\n"
            "선택: "
        )

        if user_selected_related_topic.isdecimal():
            if user_selected_related_topic <= 0 or user_selected_related_topic > len(article['related_topic']):
                print("잘못된 번호입니다. 추천 목록에 있는 번호를 입력해주세요.")
                continue

            user_selected_related_topic = int(user_selected_related_topic) - 1

            user_selected_related_topic = article['related_topic'][user_selected_related_topic]
            break

        else:
            user_selected_related_topic = generate_related_topic(article['article'], user_selected_related_topic)
            break

    search_query = user_selected_related_topic['search_query']
    search_infos = search_related_articles(search_query)

    article = recommend_related_articles(article['article'], user_selected_related_topic, search_infos)

    print("\n새로운 관련 기사를 준비하고 있습니다...\n")

