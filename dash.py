import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

def main():
    # Загрузка файла
    uploaded_file = st.file_uploader("Выберите CSV файл", type="csv")

    if uploaded_file is not None:
        # Чтение данных из CSV файла
        data = pd.read_csv(uploaded_file)
        data.rename(columns={'Количество больничных дней': 'work_days', 'Возраст': 'age', 'Пол': 'gender'}, inplace=True)

        # Проверка наличия необходимых столбцов
        if 'work_days' in data.columns and 'age' in data.columns and 'gender' in data.columns:
            # Поля для ввода параметров age и work_days
            with st.sidebar:
                st.markdown("<h3 style='font-size: 16px;'>Первая гипотеза:</h3>", unsafe_allow_html=True)
                st.markdown("<h4 style='font-size: 14px;'>Мужчины пропускают в течение года более n рабочих дней по болезни значимо чаще женщин.</h4>", unsafe_allow_html=True)
                st.markdown("<h3 style='font-size: 16px;'>Вторая гипотеза:</h3>", unsafe_allow_html=True)
                st.markdown("<h4 style='font-size: 14px;'>Работники старше X лет пропускают в течение года более n рабочих дней по болезни значимо чаще своих более молодых коллег.</h4>", unsafe_allow_html=True)

                st.markdown("<h3 style='font-size: 16px;'>Введите параметры!</h3>", unsafe_allow_html=True)
                st.markdown("<h4 style='font-size: 14px;'>Гипотеза 1</h4>", unsafe_allow_html=True)
                work_days1 = st.number_input("Введите количество рабочих дней для гипотезы 1", step=1, format="%d", help="Убедитесь, что значение находится в диапазоне предоставленных данных", key="work_days_hypothesis1")

                st.markdown("<h4 style='font-size: 14px;'>Гипотеза 2</h4>", unsafe_allow_html=True)
                age = st.number_input("Введите возраст для гипотезы 2", step=1, format="%d", help="Убедитесь, что значение находится в диапазоне предоставленных данных", key="age_hypothesis2")
                work_days2 = st.number_input("Введите количество рабочих дней для гипотезы 2", step=1, format="%d", help="Убедитесь, что значение находится в диапазоне предоставленных данных", key="work_days_hypothesis2")

            st.write("* Описание данных:")
            st.dataframe(data.describe())
            st.write("* Для проверки наших гипотез будем использовать U-критерий Манна - Уитни, в связи с тем, что нормальность распределений зависит от наших параметров")

            st.header(f"Проверка первой гипотезы")
            fig2, ax2 = plt.subplots()
            sns.histplot(data[data.work_days > work_days1], x="work_days", hue="gender", kde=True, binwidth=1, palette=['pink', 'blue'])
            plt.title(f'Распределение пропущенных дней(от {work_days1}) в зависимости от гендера')
            plt.xlabel("Количество пропущенных дней")
            plt.ylabel("Частота")
            st.pyplot(fig2)

            _,p_value = stats.mannwhitneyu(
                x=data[(data.gender == 'М') & (data.work_days > work_days1)].work_days,
                y=data[(data.gender == 'Ж') & (data.work_days > work_days1)].work_days)
            st.write("p-value:", p_value)
            st.write( "Отвергаем гипотезу, так как p_value больше уровня значимости 0.05" if p_value >= 0.05 else "Принимаем гипотезу, так как p_value меньше уровня значимости 0.05")

            st.header("Проверка второй гипотезы")
            if (age> data.age.min()):
                fig3, ax1 = plt.subplots()
                sns.set_style("darkgrid")
                sns.histplot(data=data[(data.age < age) & (data.work_days > work_days2)], x="work_days", kde=True, binwidth=1,
                             color='black')
                sns.histplot(data=data[(data.age > age) & (data.work_days > work_days2)], x="work_days", kde=True, binwidth=1,
                             color='red')
                plt.title(f'Распределение пропущенных дней( от {work_days1}) в зависимости от возраста(порог {age})')
                st.pyplot(fig3)
                _, p_value = stats.mannwhitneyu(
                    x=data[(data.age < age) & (data.work_days > work_days2)].work_days,
                    y=data[(data.age > age) & (data.work_days > work_days2)].work_days)
                st.write("p-value:", p_value)
                st.write( "Отвергаем гипотезу, так как p_value больше уровня значимости 0.05" if p_value >= 0.05 else "Принимаем гипотезу, так как p_value меньше уровня значимости 0.05")
            else:
                st.write("<span style='color:red'>Введите корректные параметры в соответствии с описанием.</span>", unsafe_allow_html=True)




        else:
            st.write("Ошибка: Файл не содержит необходимые столбцы.")
    else:
        st.write("Загрузите CSV файл.")


if __name__ == "__main__":
    main()
