import streamlit as st
import json
import plotly.express as px
import plotly.graph_objects as go
import requests
from config_setting import settings
import os

vacancies = requests.get(settings['OLIVIABI4_API_HOST'] + 'v1/vacancies/list', headers={'Authorization': 'Bearer ' + settings['OLIVIA_API_KEY']}).json()['data']['vacancies']
vacancies = {row['id']: row['name'] for row in vacancies} 
page = st.selectbox("Pick me", ["Выберите вакансию"] + list(vacancies.values()))
if page != "Выберите вакансию":
    vacancy_id = next(key for key, value in vacancies.items() if value == page)
    if os.path.exists(f'infostream/{vacancy_id}.json'):
        json_path = os.path.join(f'infostream/{vacancy_id}.json')
        with open(json_path, 'r') as my_file:
            stat = json.loads(my_file.read())
        tab_index = st.radio("Выберите вкладку", ['Общая информация', 'Информация о данных', 'Подбор параметров'])
        if tab_index == 'Общая информация':
            st.markdown(''' 
    ***Эта платформа предоставляет вам детальную информацию о кандидатах, соответствующих вашей вакансии. Кроме того, она анализирует параметры, чтобы предложить наиболее подходящие варианты и повысить эффективность подбора персонала. Мы настоятельно рекомендуем вам ознакомиться с аналитикой перед тем, как запустить вакансию. Это может помочь избежать неудачных результатов в виде отсутствия диалогов с кандидатами.
    Пожалуйста, учтите, что база кандидатов еще не является безграничной, поэтому важно воспользоваться аналитикой для более успешного подбора.***''')
            st.markdown('**P.S: Система не требует точного копирования параметров, как указано в разделе "Подбор параметров". Она предлагает помощь в расширении выборки. Если в разделе (напротив параметра) указано "Не важно", это означает, что большая часть информации о кандидатах отсутствует. Вы можете свободно регулировать выборку, добавив, например, "Дополнительные должности" - для более расширенного поиска. Или наоборот, поставив, "Не менее 1.00 года на каждом месте за последние 1 000 000 лет" на "Частоту смены работы" - чтобы найти своего Гейдельбергского Кандидата.**')
            st.markdown(''':clap:**Успехов в поиске**:clap:''')
            audio_file = 'oxxxymiron-non-fykshn_(MP3.ai).mp3'
            play_audio = st.checkbox("Воспроизводить аудио") 
            if play_audio:
                st.audio(audio_file, format='audio/wav')
        elif tab_index == 'Информация о данных':
            st.header('Информация о данных')
            # Создаем графики
            st.write(f"{stat['infopos']}")
            fig_gender = px.pie(values=list(stat['infogender'].values()), names=list(stat['infogender'].keys()))
            fig_salary = go.Figure(go.Bar(x=list(stat['infosalary'].keys()), y=list(stat['infosalary'].values()), text=list(stat['infolocation'].values()), textposition='outside'))
            fig_age = go.Figure(go.Bar(x=list(stat['infoage'].keys()), y=list(stat['infoage'].values())))
            fig_location = go.Figure(go.Bar(y=list(stat['infolocation'].keys()), x=list(stat['infolocation'].values()), orientation='h', text=list(stat['infolocation'].values()), textposition='outside'))
            fig_education = px.pie(labels=list(stat['infoeducation'].keys()), values=list(stat['infoeducation'].values()), names=list(stat['infoeducation'].keys()))
            fig_language = go.Figure(go.Bar(y=list(stat['infolanguage'].keys()), x=list(stat['infolanguage'].values()), orientation='h', text=list(stat['infolanguage'].values()), textposition='outside'))
            fig_gender.update_traces(textinfo='percent+label', pull=[0.1] * len(stat['infogender']))
            fig_education.update_traces(textinfo='percent+label', pull=[0.1] * len(stat['infoeducation']))
            # Виджет для выбора графиков
            selected_charts = st.multiselect('Выберите графики для отображения', ['Пол', 'З/П', 'Возраст', 'Локация', 'Образование', 'Языки'])
            # Отображаем выбранные графики
            for chart_name in selected_charts:
                st.subheader(f'Отображение графика: {chart_name}')
                if chart_name == 'Пол':
                    st.write('Информация данных по полу на вашу вакансию')
                    st.plotly_chart(fig_gender)
                elif chart_name == 'З/П':
                    st.write('Информация данных по зарплатным ожиданиям на вашу вакансию')
                    st.plotly_chart(fig_salary)
                elif chart_name == 'Возраст':
                    st.write('Информация данных по возрастным группам на вашу вакансию')
                    st.plotly_chart(fig_age)
                elif chart_name == 'Локация':
                    st.write('Информация данных по городам и странам на вашу вакансию')
                    st.plotly_chart(fig_location)
                elif chart_name == 'Образование':
                    st.write('Информация данных по образованию на вашу вакансию')
                    st.plotly_chart(fig_education)
                elif chart_name == 'Языки':
                    st.write('Информация данных по языкам и уровням владения на вашу вакансию')
                    st.plotly_chart(fig_language)
        elif tab_index == 'Подбор параметров':
            st.header("Подборка параметров от системы")
            st.write(f"{stat['best_params_gender']}")
            st.write(f"{stat['best_params_salary']}")
            st.write(f"{stat['best_params_age']}")
            st.write(f"{stat['best_params_location']}")
            st.write(f"{stat['best_params_education']}")
            st.write(f"{stat['best_params_language']}")
    else:
        st.header('К сожалению данных на эту вакансию пока что нет :(')
