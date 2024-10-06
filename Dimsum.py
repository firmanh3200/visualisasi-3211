import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly_express as px
import requests

st.set_page_config(layout='wide')

data = pd.read_csv(
    'data/piramida_penduduk.csv', sep=',',
    dtype={'kode_kabupaten_kota':'str', 'kelompok_umur':'str', 'tahun':'str', 'jumlah_penduduk':'float'}
)

data['kelompok_umur'] = data['kelompok_umur'].str.strip()

# Pilihan tema warna
warna1 = {
    'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 
    'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 
    'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 
    'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 
    'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 
    'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 
    'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 
    'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 
    'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 
    'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 
    'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 
    'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green', 
    'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 
    'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 
}
warna2 = {
    'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgrey', 
    'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 
    'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 
    'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 
    'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 
    'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 
    'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 
    'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 
    'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 
    'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 
    'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 
    'whitesmoke', 'yellow', 'yellowgreen'
}

pivot_kabkot = data.pivot_table(
    values='jumlah_penduduk', 
    index=['tahun', 'kelompok_umur', 'nama_kabupaten_kota'], 
    columns='jenis_kelamin'
).reset_index().sort_values(by=['tahun', 'kelompok_umur'])

st.title("Visualisasi Data Kabupaten Sumedang")
st.subheader("", divider='rainbow')

st.subheader(":blue[Piramida Penduduk]")

with st.container(border=True):
    kolom1, kolom2 = st.columns(2)
    
    with kolom1:
        pilihwarna1 = st.selectbox("Pilih Tema Warna1:", options=list(warna1), key='warna1')
    
    with kolom2:
        pilihwarna2 = st.selectbox("Pilih Tema Warna2:", options=list(warna2), key='warna2')
    
            
if pilihwarna1 and pilihwarna2:
    kol1, kol2 = st.columns(2)
    
    with kol1:
        with st.container(border=True):
            pilihantahun = pivot_kabkot['tahun'].unique()
            
            kolc, kold = st.columns(2)
            with kolc:
                tahunterpilih = st.selectbox("Filter Tahun", pilihantahun)
            
            df1 = pivot_kabkot[(pivot_kabkot['tahun'] == tahunterpilih)]
            df1['LAKI-LAKI'] = df1['LAKI-LAKI'] * -1
        
            piramida_kabkot = px.bar(df1, x=['LAKI-LAKI', 'PEREMPUAN'], 
                                    y='kelompok_umur', labels={'variable':''},
                                orientation='h', 
                                color_discrete_map={'LAKI-LAKI':pilihwarna1, 'PEREMPUAN':pilihwarna2})
            
            # Menempatkan legenda di bawah tengah
            piramida_kabkot.update_layout(
                xaxis_title="",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            st.subheader(f"Piramida Penduduk :blue[Kabupaten Sumedang], :green[Tahun {tahunterpilih}]")
            st.plotly_chart(piramida_kabkot, use_container_width=True)
            with st.expander("Tabel"):
                st.dataframe(df1, use_container_width=True, hide_index=True)
    
    with kol2:
        with st.container(border=True):
            df2 = pivot_kabkot.copy()
            df2['LAKI-LAKI'] = df2['LAKI-LAKI'] * -1
        
            animasi_kabkot = px.bar(df2, x=['LAKI-LAKI', 'PEREMPUAN'], 
                                    y='kelompok_umur', labels={'variable':''},
                                orientation='h',
                                animation_frame='tahun', 
                                color_discrete_map={'LAKI-LAKI':pilihwarna1, 'PEREMPUAN':pilihwarna2})
            
            # Menempatkan legenda di bawah tengah
            animasi_kabkot.update_layout(
                xaxis_title="",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            st.subheader(f"Animasi Piramida Penduduk :blue[Kabupaten Sumedang]")
            st.plotly_chart(animasi_kabkot, use_container_width=True)
              
st.subheader("", divider='rainbow')

kol1, kol2, kol3, kol4, kol5 = st.columns(5)
with kol1:
    st.link_button("Sumber Data", url="https://opendata.jabarprov.go.id/id/dataset/jumlah-penduduk-berdasarkan-kelompok-umur-dan-kabupatenkota-di-jawa-barat")
with kol2:
    st.link_button("Sumber Peta Dasar", url="https://github.com/Alf-Anas/batas-administrasi-indonesia") 
with kol3:
    st.link_button("Inspirasi Grafik", url="https://plotly.com/python")
with kol4:
    st.link_button("Framework", url="https://streamlit.io")
with kol5:
    st.link_button("Pengolah Data", url="https://pandas.pydata.org/")
st.subheader("", divider='rainbow')
