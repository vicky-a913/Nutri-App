# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime
import json

# Configuración de la página
st.set_page_config(
    page_title="NutriTrack Chihuahua",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Datos de ejemplo (en una aplicación real, cargarías desde CSV/BD)
@st.cache_data
def load_sample_data():
    # Datos de seguridad alimentaria por municipio
    municipios_data = {
        'Municipio': ['Chihuahua', 'Juárez', 'Delicias', 'Cuauhtémoc', 'Parral', 'Camargo', 'Jiménez', 'Casas Grandes'],
        'Población': [1000000, 1500000, 150000, 200000, 120000, 50000, 45000, 60000],
        'Seguridad_Alimentaria': [75, 65, 60, 70, 55, 50, 45, 40],  # Porcentaje
        'Obesidad_Adultos': [32, 35, 38, 34, 36, 40, 42, 45],
        'Desnutrición_Infantil': [8, 12, 15, 10, 18, 20, 22, 25],
        'Acceso_Alimentos_Saludables': [80, 70, 60, 65, 55, 50, 45, 40],
        'Ingreso_Promedio': [25000, 22000, 18000, 20000, 16000, 15000, 14000, 13000]
    }
    
    # Datos de alimentos regionales
    alimentos_data = {
        'Alimento': ['Manzana', 'Nuez', 'Carne Seca', 'Queso Menonita', 'Frijol', 'Maíz', 'Chile', 'Tomate'],
        'Calorías': [52, 654, 350, 400, 347, 365, 40, 18],
        'Proteína_g': [0.3, 15, 45, 25, 21, 9, 2, 0.9],
        'Carbohidratos_g': [14, 13, 3, 2, 63, 74, 9, 4],
        'Grasas_g': [0.2, 65, 18, 33, 1, 4, 0.4, 0.2],
        'Categoria': ['Fruta', 'Fruto Seco', 'Proteína', 'Lácteo', 'Legumbre', 'Cereal', 'Verdura', 'Verdura'],
        'Precio_Promedio': [25, 120, 200, 150, 30, 20, 35, 28]
    }
    
    # Datos temporales de hábitos alimenticios
    años = list(range(2010, 2024))
    tendencias_data = {
        'Año': años,
        'Consumo_Frutas_Verduras': [45, 47, 48, 50, 52, 53, 55, 54, 56, 58, 57, 55, 53, 52],
        'Consumo_Alimentos_Procesados': [35, 37, 40, 42, 45, 48, 50, 52, 55, 53, 50, 48, 45, 43],
        'Obesidad_Poblacion': [28, 29, 30, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
        'Gasto_Alimentacion_Familiar': [1200, 1250, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400]
    }
    
    return pd.DataFrame(municipios_data), pd.DataFrame(alimentos_data), pd.DataFrame(tendencias_data)

# Funciones de cálculo nutricional
def calcular_IMC(peso, altura):
    """Calcula el Índice de Masa Corporal"""
    return peso / ((altura / 100) ** 2)

def calcular_tasa_metabolica_basal(edad, peso, altura, genero):
    """Calcula la Tasa Metabólica Basal usando la ecuación de Mifflin-St Jeor"""
    if genero == "Masculino":
        tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * edad - 161
    return tmb

def calcular_calorias_diarias(tmb, nivel_actividad, objetivo):
    """Calcula las calorías diarias necesarias"""
    factores_actividad = {
        "Sedentario": 1.2,
        "Ligero": 1.375,
        "Moderado": 1.55,
        "Activo": 1.725,
        "Muy activo": 1.9
    }
    
    factores_objetivo = {
        "Bajar peso": 0.85,
        "Mantener peso": 1.0,
        "Subir peso": 1.15
    }
    
    return tmb * factores_actividad[nivel_actividad] * factores_objetivo[objetivo]

# Interfaz principal
def main():
    # Cargar datos
    df_municipios, df_alimentos, df_tendencias = load_sample_data()
    
    # Sidebar
    st.sidebar.title("🥗 NutriTrack Chihuahua")
    st.sidebar.markdown("---")
    
    modulo = st.sidebar.selectbox(
        "Selecciona el módulo:",
        ["Dashboard Nutricional", "Calculadora Personal", "Alimentos Regionales", "Tendencias Alimentarias"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Fuentes de datos:**
    - ENSANUT 2023
    - INEGI
    - Secretaría de Salud
    - Tablas nutricionales oficiales
    """)
    
    # Módulo 1: Dashboard Nutricional
    if modulo == "Dashboard Nutricional":
        st.title("📊 Dashboard Nutricional - Estado de Chihuahua")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Seguridad Alimentaria Promedio", f"{df_municipios['Seguridad_Alimentaria'].mean():.1f}%")
        with col2:
            st.metric("Prevalencia de Obesidad", f"{df_municipios['Obesidad_Adultos'].mean():.1f}%")
        with col3:
            st.metric("Desnutrición Infantil", f"{df_municipios['Desnutrición_Infantil'].mean():.1f}%")
        
        st.markdown("---")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            municipio_seleccionado = st.selectbox("Selecciona municipio:", df_municipios['Municipio'])
        with col2:
            indicador = st.selectbox("Indicador a visualizar:", 
                                   ['Seguridad_Alimentaria', 'Obesidad_Adultos', 'Desnutrición_Infantil', 'Acceso_Alimentos_Saludables'])
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Mapa de calor de indicadores
            fig = px.bar(df_municipios, x='Municipio', y=indicador,
                        title=f'{indicador.replace("_", " ")} por Municipio',
                        color=indicador, color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Scatter plot: Seguridad alimentaria vs Ingreso
            fig = px.scatter(df_municipios, x='Ingreso_Promedio', y='Seguridad_Alimentaria',
                           size='Población', color='Municipio', hover_name='Municipio',
                           title='Relación: Ingreso vs Seguridad Alimentaria')
            st.plotly_chart(fig, use_container_width=True)
        
        # Datos del municipio seleccionado
        municipio_data = df_municipios[df_municipios['Municipio'] == municipio_seleccionado].iloc[0]
        
        st.subheader(f"📋 Perfil Nutricional: {municipio_seleccionado}")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Seguridad Alimentaria", f"{municipio_data['Seguridad_Alimentaria']}%")
        with col2:
            st.metric("Obesidad en Adultos", f"{municipio_data['Obesidad_Adultos']}%")
        with col3:
            st.metric("Desnutrición Infantil", f"{municipio_data['Desnutrición_Infantil']}%")
        with col4:
            st.metric("Acceso Alimentos Saludables", f"{municipio_data['Acceso_Alimentos_Saludables']}%")
    
    # Módulo 2: Calculadora Personal
    elif modulo == "Calculadora Personal":
        st.title("🧮 Calculadora Nutricional Personalizada")
        
        st.markdown("""
        Complete la siguiente información para obtener recomendaciones nutricionales personalizadas 
        basadas en sus características y objetivos.
        """)
        
        with st.form("calculadora_nutricional"):
            col1, col2 = st.columns(2)
            
            with col1:
                edad = st.slider("Edad", 18, 80, 30)
                peso = st.number_input("Peso (kg)", 40.0, 150.0, 70.0)
                altura = st.number_input("Altura (cm)", 140.0, 220.0, 170.0)
            
            with col2:
                genero = st.selectbox("Género", ["Masculino", "Femenino"])
                nivel_actividad = st.selectbox("Nivel de actividad", 
                                             ["Sedentario", "Ligero", "Moderado", "Activo", "Muy activo"])
                objetivo = st.selectbox("Objetivo", ["Bajar peso", "Mantener peso", "Subir peso"])
            
            submitted = st.form_submit_button("Calcular Recomendaciones")
            
            if submitted:
                # Cálculos
                imc = calcular_IMC(peso, altura)
                tmb = calcular_tasa_metabolica_basal(edad, peso, altura, genero)
                calorias_diarias = calcular_calorias_diarias(tmb, nivel_actividad, objetivo)
                
                # Resultados
                st.success("¡Cálculos completados! Aquí están sus recomendaciones:")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("IMC", f"{imc:.1f}")
                with col2:
                    st.metric("TMB", f"{tmb:.0f} kcal")
                with col3:
                    st.metric("Calorías Diarias", f"{calorias_diarias:.0f} kcal")
                
                # Interpretación IMC
                st.subheader("📈 Interpretación de su IMC")
                if imc < 18.5:
                    st.warning("Bajo peso - Consulte con un especialista")
                elif imc < 25:
                    st.success("Peso normal - ¡Excelente!")
                elif imc < 30:
                    st.warning("Sobrepeso - Se recomienda atención")
                else:
                    st.error("Obesidad - Consulte con un especialista")
                
                # Recomendaciones nutricionales
                st.subheader("🥗 Recomendaciones Nutricionales Diarias")
                
                # Distribución de macronutrientes basada en objetivo
                if objetivo == "Bajar peso":
                    distribucion = {"Proteína": 30, "Carbohidratos": 40, "Grasas": 30}
                elif objetivo == "Mantener peso":
                    distribucion = {"Proteína": 25, "Carbohidratos": 50, "Grasas": 25}
                else:  # Subir peso
                    distribucion = {"Proteína": 30, "Carbohidratos": 45, "Grasas": 25}
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    proteina_g = (calorias_diarias * distribucion["Proteína"] / 100) / 4
                    st.metric("Proteína", f"{proteina_g:.1f}g")
                with col2:
                    carbohidratos_g = (calorias_diarias * distribucion["Carbohidratos"] / 100) / 4
                    st.metric("Carbohidratos", f"{carbohidratos_g:.1f}g")
                with col3:
                    grasas_g = (calorias_diarias * distribucion["Grasas"] / 100) / 9
                    st.metric("Grasas", f"{grasas_g:.1f}g")
                
                # Ejemplo de plan alimenticio
                st.subheader("🍽️ Ejemplo de Plan Alimenticio Diario")
                plan_data = {
                    'Comida': ['Desayuno', 'Almuerzo', 'Comida', 'Merienda', 'Cena'],
                    'Calorías': [calorias_diarias*0.25, calorias_diarias*0.10, calorias_diarias*0.35, 
                               calorias_diarias*0.10, calorias_diarias*0.20],
                    'Ejemplo': [
                        'Huevos + Pan integral + Fruta',
                        'Yogurt + Nueces',
                        'Pechuga + Arroz + Ensalada',
                        'Manzana + Queso',
                        'Pescado + Verduras al vapor'
                    ]
                }
                df_plan = pd.DataFrame(plan_data)
                df_plan['Calorías'] = df_plan['Calorías'].round(0)
                st.dataframe(df_plan, use_container_width=True)
    
    # Módulo 3: Alimentos Regionales
    elif modulo == "Alimentos Regionales":
        st.title("🌮 Base de Datos de Alimentos Regionales")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            categoria_filtro = st.selectbox("Filtrar por categoría", 
                                          ["Todas"] + list(df_alimentos['Categoria'].unique()))
        with col2:
            min_calorias, max_calorias = st.slider("Rango de calorías", 
                                                  int(df_alimentos['Calorías'].min()), 
                                                  int(df_alimentos['Calorías'].max()),
                                                  (0, 700))
        with col3:
            buscar_alimento = st.text_input("Buscar alimento")
        
        # Aplicar filtros
        df_filtrado = df_alimentos.copy()
        if categoria_filtro != "Todas":
            df_filtrado = df_filtrado[df_filtrado['Categoria'] == categoria_filtro]
        
        df_filtrado = df_filtrado[
            (df_filtrado['Calorías'] >= min_calorias) & 
            (df_filtrado['Calorías'] <= max_calorias)
        ]
        
        if buscar_alimento:
            df_filtrado = df_filtrado[
                df_filtrado['Alimento'].str.contains(buscar_alimento, case=False)
            ]
        
        # Mostrar tabla de alimentos
        st.subheader("📋 Alimentos Filtrados")
        st.dataframe(df_filtrado, use_container_width=True)
        
        # Gráficos de comparación
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(df_filtrado, x='Alimento', y='Calorías', 
                        title='Calorías por Alimento', color='Categoria')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico de radar para alimento seleccionado
            alimento_seleccionado = st.selectbox("Selecciona alimento para análisis detallado:", 
                                               df_filtrado['Alimento'])
            
            if alimento_seleccionado:
                alimento_data = df_filtrado[df_filtrado['Alimento'] == alimento_seleccionado].iloc[0]
                
                categorias = ['Calorías', 'Proteína_g', 'Carbohidratos_g', 'Grasas_g']
                valores = [
                    alimento_data['Calorías'] / 700,  # Normalizado
                    alimento_data['Proteína_g'] / 50,
                    alimento_data['Carbohidratos_g'] / 100,
                    alimento_data['Grasas_g'] / 70
                ]
                
                fig = go.Figure(data=go.Scatterpolar(
                    r=valores + [valores[0]],  # Cerrar el círculo
                    theta=categorias + [categorias[0]],
                    fill='toself',
                    name=alimento_seleccionado
                ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                    showlegend=False,
                    title=f"Perfil Nutricional: {alimento_seleccionado}"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Recetas saludables
        st.subheader("🍳 Recetas Saludables con Alimentos Locales")
        
        recetas = {
            "Ensalada de Nuez y Manzana": {
                "ingredientes": ["Manzana", "Nuez", "Queso Menonita", "Lechuga"],
                "calorias": 320,
                "preparacion": "Mezclar todos los ingredientes frescos"
            },
            "Guiso de Frijol con Chile": {
                "ingredientes": ["Frijol", "Chile", "Tomate", "Cebolla"],
                "calorias": 450,
                "preparacion": "Cocinar los frijoles y agregar verduras picadas"
            }
        }
        
        for receta, info in recetas.items():
            with st.expander(f"🍴 {receta} - {info['calorias']} kcal"):
                st.write("**Ingredientes:**", ", ".join(info['ingredientes']))
                st.write("**Preparación:**", info['preparacion'])
    
    # Módulo 4: Tendencias Alimentarias
    else:
        st.title("📈 Tendencias Alimentarias 2010-2023")
        
        # Selector de indicadores
        indicadores = ['Consumo_Frutas_Verduras', 'Consumo_Alimentos_Procesados', 
                      'Obesidad_Poblacion', 'Gasto_Alimentacion_Familiar']
        
        col1, col2 = st.columns(2)
        with col1:
            indicador1 = st.selectbox("Indicador 1", indicadores, index=0)
        with col2:
            indicador2 = st.selectbox("Indicador 2", indicadores, index=1)
        
        # Gráfico de tendencias
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_tendencias['Año'], 
            y=df_tendencias[indicador1],
            name=indicador1.replace('_', ' '),
            line=dict(color='blue')
        ))
        
        fig.add_trace(go.Scatter(
            x=df_tendencias['Año'], 
            y=df_tendencias[indicador2],
            name=indicador2.replace('_', ' '),
            line=dict(color='red'),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title=f"Evolución de Indicadores Alimentarios",
            xaxis=dict(title='Año'),
            yaxis=dict(title=indicador1.replace('_', ' '), side='left'),
            yaxis2=dict(title=indicador2.replace('_', ' '), side='right', overlaying='y'),
            legend=dict(x=0, y=1.1, orientation='h')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Análisis de correlación
        st.subheader("🔍 Análisis de Correlación")
        
        correlacion = df_tendencias[indicador1].corr(df_tendencias[indicador2])
        
        col1, col2, col3 = st.columns(3)
        with col2:
            st.metric("Coeficiente de Correlación", f"{correlacion:.3f}")
        
        # Interpretación de correlación
        if abs(correlacion) > 0.7:
            interpretacion = "Fuerte correlación"
            color = "red" if correlacion < 0 else "green"
        elif abs(correlacion) > 0.3:
            interpretacion = "Correlación moderada"
            color = "orange"
        else:
            interpretacion = "Correlación débil"
            color = "blue"
        
        st.info(f"**Interpretación:** {interpretacion} entre los indicadores seleccionados.")
        
        # Proyecciones
        st.subheader("📊 Proyecciones 2024-2030")
        
        # Simulación simple de proyección
        años_proyeccion = list(range(2024, 2031))
        ultimo_valor = df_tendencias[indicador1].iloc[-1]
        tendencia = (df_tendencias[indicador1].iloc[-1] - df_tendencias[indicador1].iloc[-5]) / 5
        
        proyecciones = [ultimo_valor + tendencia * (i+1) for i in range(len(años_proyeccion))]
        
        fig_proy = px.line(x=años_proyeccion, y=proyecciones, 
                          title=f"Proyección {indicador1.replace('_', ' ')} 2024-2030",
                          labels={'x': 'Año', 'y': indicador1.replace('_', ' ')})
        
        st.plotly_chart(fig_proy, use_container_width=True)

if __name__ == "__main__":
    main()
