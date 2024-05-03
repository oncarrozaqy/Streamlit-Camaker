import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df = pd.read_excel('DataDummyStreamlit.xlsx')

if df is not None:
    st.title('Dashboard ITB Tracer Study')

    # Navigasi Tahun
    tahun = st.sidebar.slider('Pilih Tahun', min_value=2018, max_value=2019)
    df_filtered = df[df['Tahun Survey'] == tahun]

    # Navigasi Fakultas
    fakultas_list = df['Fakultas'].unique().tolist()
    fakultas_list.sort()
    fakultas_list.insert(0, 'All')  
    selected_fakultas = st.sidebar.selectbox('Pilih Fakultas', fakultas_list)

    # Navigasi Program Studi
    if selected_fakultas != 'All':
        df_filtered = df_filtered[df_filtered['Fakultas'] == selected_fakultas]
        prodi_list = df_filtered['Prodi'].unique().tolist()
        prodi_list.sort()
        prodi_list.insert(0, 'All')  
        selected_prodi = st.sidebar.selectbox('Pilih Program Studi', prodi_list)
        if selected_prodi != 'All':
            df_filtered = df_filtered[df_filtered['Prodi'] == selected_prodi]
    else:
        prodi_list = df_filtered['Prodi'].unique().tolist()
        prodi_list.sort()
        prodi_list.insert(0, 'All')  
        selected_prodi = st.sidebar.selectbox('Pilih Program Studi', prodi_list)
        if selected_prodi != 'All':
            df_filtered = df_filtered[df_filtered['Prodi'] == selected_prodi]

    # Membagi kelas IP
    bins = [2, 2.5, 3, 3.5, 4]
    labels = ['2-2.5', '2.51-3.0', '3.01-3.50', '3.51-4.0']
    df_filtered['IP Class'] = pd.cut(df_filtered['IP'], bins=bins, labels=labels)

    #  Grafik dengan Plotly
    
    #  Rata-rata IP
    st.subheader('Indeks Prestasi (IP)')
    fig_ip = px.histogram(df_filtered,
                        y='IP Class', 
                        histfunc='count', 
                        labels={
                            'IP Class':'IP Range', 
                            'count':'Count'
                            }
                        )

    fig_ip.update_layout(
        yaxis={
            'categoryorder':'array', 
            'categoryarray':labels
        },
        font_family="Nunito, sans-serif",
    )

    st.plotly_chart(fig_ip)


    # IP Rata-rata per prodi
    st.subheader('Rata-rata IP per Program Studi')
    ip_rata_prodi = df_filtered.groupby('Prodi')['IP'].mean().sort_values().reset_index()

    fig_ip_rata_prodi = px.bar(
        ip_rata_prodi, 
        x='IP', y='Prodi',
        width=600, 
        height=1000, 
        labels={
            'Prodi':'Program Studi', 
            'IP':'Rata-rata IP'
        }
    )
    
    prodi_counts = df_filtered['Prodi'].value_counts()
    fig_ip_rata_prodi.update_yaxes(
        tickmode='array',
        tickvals=np.arange(len(prodi_counts)),
        ticktext=[
            f"{prodi} ({count})" for prodi, count in prodi_counts.items()
        ]
    )
    
    fig_ip_rata_prodi.update_traces(
        text=ip_rata_prodi['IP'].round(2),
        textposition='outside'
    )
    fig_ip_rata_prodi.update_layout(
        font_family="Nunito, sans-serif",   
    )
    st.plotly_chart(fig_ip_rata_prodi, use_container_width=True) 

    # Boxplot IP
    st.subheader('Boxplot Indeks Prestasi (IP)')
    fig_boxplot = px.box(
        df_filtered, 
        y='IP', 
        labels={
            'IP':'Indeks Prestasi (IP)'
            }
    )
    fig_boxplot.update_layout(
        font_family="Nunito, sans-serif", 
    )
    st.plotly_chart(fig_boxplot)

    #  Pekerjaan Utama
    st.subheader(' Pekerjaan Utama')
    pekerjaan_count = df_filtered['Pekerjaan Utama'].value_counts()
    fig_pekerjaan = px.pie(
        values=pekerjaan_count.values, 
        names=pekerjaan_count.index, 
        labels={
            'x':'Pekerjaan Utama', 
            'y':'Count'
            }
    )
    fig_pekerjaan.update_layout(
        font_family="Nunito, sans-serif",     
    )
    st.plotly_chart(fig_pekerjaan)

    # Pekerjaan Utama Per Prodi
    st.subheader('Pekerjaan Utama Per Prodi')
    fig_pekerjaan_prodi = px.histogram(
        df_filtered.groupby(['Prodi', 'Pekerjaan Utama']).size().reset_index(name='Count'), 
        y='Prodi', 
        x='Count', 
        color='Pekerjaan Utama',
        barnorm='percent', 
        orientation='h',
        width=900, 
        height=1200,
        labels={
            'Prodi':'Program Studi', 
            'Count':'Persentase Pekerjaan Utama'
        },
        category_orders={"Pekerjaan Utama": ["Bekerja", "Bekerja dan wiraswasta", "Wirausaha"]} 
    )
    
    counts_prodi = df_filtered['Prodi'].value_counts()
    fig_pekerjaan_prodi.update_yaxes(
        tickmode='array',
        tickvals=np.arange(len(counts_prodi)),
        ticktext=[
            f"{prodi} ({count}/{counts_prodi[prodi]})" for prodi, count in counts_prodi.items()
        ]
    )

    fig_pekerjaan_prodi.update_traces(
        texttemplate='%{x:.2f}%', 
        textposition='inside'  
    )
    
    fig_pekerjaan_prodi.update_layout(
        font_family="Nunito, sans-serif",  
    )
    
    st.plotly_chart(fig_pekerjaan_prodi)
