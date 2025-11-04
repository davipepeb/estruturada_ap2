import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os

# Configuração da página
st.set_page_config(
    page_title="Spa Dashboard - Análise Sazonal e Precificação",
    page_icon="💆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carrega os dados sazonais
def load_seasonal_data():
    """Carrega os dados sazonais do arquivo CSV"""
    df = pd.read_csv('dados_sazonais.csv')
    return df

# Carrega o histórico de cálculos
def load_pricing_history():
    """Carrega o histórico de cálculos de precificação"""
    if os.path.exists('historico_precificacao.json'):
        with open('historico_precificacao.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Salva o histórico de cálculos
def save_pricing_history(history):
    """Salva o histórico de cálculos"""
    with open('historico_precificacao.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# CSS personalizado
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-card {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
    }
    .warning-card {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
    }
    .favorite-card {
        background-color: #fff8e1;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffb300;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.title("💆 Spa Dashboard - Análise Sazonal e Precificação Inteligente")
st.markdown("---")

# Carrega dados
seasonal_data = load_seasonal_data()
pricing_history = load_pricing_history()

# Sidebar com navegação
st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Selecione uma página:",
    ["📊 Análise Sazonal", "💰 Precificação Inteligente", "📈 Histórico de Cálculos"]
)

# Meses para referência
months = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

# ============================================================================
# PÁGINA 1: ANÁLISE SAZONAL
# ============================================================================
if page == "📊 Análise Sazonal":
    st.header("Análise Sazonal de Demanda")
    st.markdown("Visualize a demanda média mensal e o desvio padrão dos serviços")
    st.markdown("---")
    
    # Separa dados por serviço
    drainage_data = seasonal_data[seasonal_data['Servico'] == 'Drenagem Linfática corporal (50 min)'].sort_values('Mes')
    massage_data = seasonal_data[seasonal_data['Servico'] == 'Massagem Relaxante (50 min)'].sort_values('Mes')
    
    # Cria abas
    tab1, tab2 = st.tabs(["Drenagem Linfática", "Massagem Relaxante"])
    
    # ========== TAB 1: DRENAGEM LINFÁTICA ==========
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Demanda Mensal")
            
            # Gráfico de linha para demanda
            fig_demand = go.Figure()
            fig_demand.add_trace(go.Scatter(
                x=[months[m] for m in drainage_data['Mes']],
                y=drainage_data['Media'],
                mode='lines+markers',
                name='Demanda Média',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=8)
            ))
            
            fig_demand.update_layout(
                title="Demanda Média de Drenagens por Mês",
                xaxis_title="Mês",
                yaxis_title="Quantidade de Atendimentos",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig_demand, use_container_width=True)
        
        with col2:
            st.subheader("📊 Desvio Padrão")
            
            # Gráfico de barras para desvio padrão
            fig_std = go.Figure()
            fig_std.add_trace(go.Bar(
                x=[months[m] for m in drainage_data['Mes']],
                y=drainage_data['Desvio_padrao'],
                name='Desvio Padrão',
                marker=dict(color='#2ca02c')
            ))
            
            fig_std.update_layout(
                title="Variação da Demanda (Desvio Padrão)",
                xaxis_title="Mês",
                yaxis_title="Desvio Padrão",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig_std, use_container_width=True)
        
        # Tabela com dados
        st.subheader("Dados Detalhados")
        display_data = drainage_data.copy()
        display_data['Mes'] = display_data['Mes'].map(months)
        display_data = display_data[['Mes', 'Media', 'Desvio_padrao']].rename(
            columns={'Mes': 'Mês', 'Media': 'Demanda Média', 'Desvio_padrao': 'Desvio Padrão'}
        )
        st.dataframe(display_data, use_container_width=True, hide_index=True)
    
    # ========== TAB 2: MASSAGEM RELAXANTE ==========
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Demanda Mensal")
            
            # Gráfico de linha para demanda
            fig_demand = go.Figure()
            fig_demand.add_trace(go.Scatter(
                x=[months[m] for m in massage_data['Mes']],
                y=massage_data['Media'],
                mode='lines+markers',
                name='Demanda Média',
                line=dict(color='#ff7f0e', width=3),
                marker=dict(size=8)
            ))
            
            fig_demand.update_layout(
                title="Demanda Média de Massagens por Mês",
                xaxis_title="Mês",
                yaxis_title="Quantidade de Atendimentos",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig_demand, use_container_width=True)
        
        with col2:
            st.subheader("📊 Desvio Padrão")
            
            # Gráfico de barras para desvio padrão
            fig_std = go.Figure()
            fig_std.add_trace(go.Bar(
                x=[months[m] for m in massage_data['Mes']],
                y=massage_data['Desvio_padrao'],
                name='Desvio Padrão',
                marker=dict(color='#d62728')
            ))
            
            fig_std.update_layout(
                title="Variação da Demanda (Desvio Padrão)",
                xaxis_title="Mês",
                yaxis_title="Desvio Padrão",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig_std, use_container_width=True)
        
        # Tabela com dados
        st.subheader("Dados Detalhados")
        display_data = massage_data.copy()
        display_data['Mes'] = display_data['Mes'].map(months)
        display_data = display_data[['Mes', 'Media', 'Desvio_padrao']].rename(
            columns={'Mes': 'Mês', 'Media': 'Demanda Média', 'Desvio_padrao': 'Desvio Padrão'}
        )
        st.dataframe(display_data, use_container_width=True, hide_index=True)

# ============================================================================
# PÁGINA 2: PRECIFICAÇÃO INTELIGENTE
# ============================================================================
elif page == "💰 Precificação Inteligente":
    st.header("Precificação Inteligente")
    st.markdown("Calcule preços promocionais para atingir suas metas de lucro")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    # ========== COLUNA 1: FORMULÁRIO ==========
    with col1:
        st.subheader("⚙️ Configuração")
        
        # Seleção de serviço
        service = st.selectbox(
            "Selecione o Serviço",
            ["Drenagem Linfática corporal (50 min)", "Massagem Relaxante (50 min)"]
        )
        
        # Seleção de mês
        current_month = st.selectbox(
            "Mês Atual",
            list(months.values()),
            index=datetime.now().month - 1
        )
        current_month_num = list(months.values()).index(current_month) + 1
        
        # Busca dados do mês selecionado
        month_data = seasonal_data[
            (seasonal_data['Servico'] == service) & 
            (seasonal_data['Mes'] == current_month_num)
        ]
        
        if not month_data.empty:
            demand = month_data['Media'].values[0]
            std_dev = month_data['Desvio_padrao'].values[0]
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>📊 Dados do Mês</h4>
                <p><strong>Demanda Esperada:</strong> {int(demand)} massagens</p>
                <p><strong>Desvio Padrão:</strong> ±{std_dev:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Inputs do formulário
        original_price = st.number_input(
            "Preço Original (R$)",
            min_value=0.0,
            value=100.0,
            step=0.01,
            format="%.2f"
        )
        
        service_cost = st.number_input(
            "Custo por Serviço (R$)",
            min_value=0.0,
            value=20.0,
            step=0.01,
            format="%.2f",
            help="Custo do spa para realizar o serviço (materiais, energia, etc)"
        )
        
        commission_percentage = st.number_input(
            "Comissão Massagista (%)",
            min_value=0.0,
            max_value=100.0,
            value=40.0,
            step=0.1,
            format="%.1f"
        )
        
        desired_profit_increase = st.number_input(
            "Lucro Adicional Desejado (%)",
            min_value=0.0,
            value=20.0,
            step=0.1,
            format="%.1f"
        )
        
        promotional_price = st.number_input(
            "Preço Promocional (R$)",
            min_value=0.0,
            value=80.0,
            step=0.01,
            format="%.2f"
        )
        
        st.markdown("---")
        
        # Botão de cálculo
        calculate_button = st.button("🧮 Calcular", use_container_width=True, type="primary")
    
    # ========== COLUNA 2: RESULTADOS ==========
    with col2:
        if calculate_button and not month_data.empty:
            demand = month_data['Media'].values[0]
            
            # Cálculos
            commission_decimal = commission_percentage / 100
            profit_increase_decimal = desired_profit_increase / 100
            
            # ===== CENÁRIO SEM PROMOÇÃO =====
            revenue_without_promo = original_price * demand
            total_costs_without_promo = (commission_percentage / 100 * revenue_without_promo) + (service_cost * demand)
            spa_revenue_without_promo = revenue_without_promo - total_costs_without_promo
            
            commission_without_promo = (commission_percentage / 100) * revenue_without_promo
            total_service_cost_without_promo = service_cost * demand
            
            # ===== META DE LUCRO =====
            desired_spa_revenue = spa_revenue_without_promo * (1 + profit_increase_decimal)
            
            # ===== CENÁRIO COM PROMOÇÃO =====
            # Lucro por serviço com preço promocional = preço - comissão - custo
            profit_per_promo_service = promotional_price - (promotional_price * commission_decimal) - service_cost
            required_quantity = int(desired_spa_revenue / profit_per_promo_service) + 1
            
            # Comissão final
            total_promo_revenue = promotional_price * required_quantity
            final_commission = total_promo_revenue * commission_decimal
            total_service_cost_with_promo = service_cost * required_quantity
            spa_revenue_with_promo = total_promo_revenue - final_commission - total_service_cost_with_promo
            
            # Exibe resultados
            st.subheader("📈 Análise Sem Promoção")
            st.markdown(f"""
            <div class="success-card">
                <h4>Cenário Atual (Preço Normal)</h4>
                <p><strong>Demanda Esperada:</strong> {int(demand)} massagens</p>
                <p><strong>Receita Total:</strong> R$ {revenue_without_promo:,.2f}</p>
                <p><strong>Comissão Massagista:</strong> R$ {commission_without_promo:,.2f}</p>
                <p><strong>Custo por Serviço:</strong> R$ {total_service_cost_without_promo:,.2f}</p>
                <p style="font-weight: bold; font-size: 16px; color: #155724;"><strong>Lucro Real do Spa:</strong> R$ {spa_revenue_without_promo:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("🎯 Meta de Lucro com Promoção")
            st.markdown(f"""
            <div class="warning-card">
                <h4>Cenário Promocional</h4>
                <p><strong>Lucro Necessário:</strong> R$ {desired_spa_revenue:,.2f}</p>
                <p style="font-size: 24px; font-weight: bold; color: #ff6b6b; margin: 15px 0;">
                    Você precisa vender {required_quantity} massagens
                </p>
                <p style="font-size: 14px; color: #666;">ao preço promocional de R$ {promotional_price:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Receita Total", f"R$ {total_promo_revenue:,.2f}")
            with col_b:
                st.metric("Comissão", f"R$ {final_commission:,.2f}")
            with col_c:
                st.metric("Custo Serviço", f"R$ {total_service_cost_with_promo:,.2f}")
            
            st.metric("💰 Lucro Real com Promoção", f"R$ {spa_revenue_with_promo:,.2f}", delta=f"{((spa_revenue_with_promo / spa_revenue_without_promo - 1) * 100):.1f}%" if spa_revenue_without_promo > 0 else "0%")
            
            # Botão para salvar cálculo
            if st.button("💾 Salvar Cálculo no Histórico", use_container_width=True):
                new_calculation = {
                    "id": len(pricing_history),
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "servico": service,
                    "mes": current_month,
                    "preco_original": original_price,
                    "custo_servico": service_cost,
                    "comissao_percentual": commission_percentage,
                    "lucro_adicional": desired_profit_increase,
                    "preco_promocional": promotional_price,
                    "demanda": int(demand),
                    "receita_sem_promo": revenue_without_promo,
                    "comissao_sem_promo": commission_without_promo,
                    "custo_sem_promo": total_service_cost_without_promo,
                    "lucro_sem_promo": spa_revenue_without_promo,
                    "lucro_necessario": desired_spa_revenue,
                    "quantidade_necessaria": required_quantity,
                    "receita_com_promo": total_promo_revenue,
                    "comissao_com_promo": final_commission,
                    "custo_com_promo": total_service_cost_with_promo,
                    "lucro_com_promo": spa_revenue_with_promo,
                    "favorito": False
                }
                
                pricing_history.append(new_calculation)
                save_pricing_history(pricing_history)
                
                st.success("✅ Cálculo salvo com sucesso! Vá para a aba 'Histórico de Cálculos' para visualizar.")
        
        elif not month_data.empty:
            st.info("👈 Preencha os dados e clique em 'Calcular' para ver os resultados")
        else:
            st.error("❌ Dados não encontrados para este mês e serviço")

# ============================================================================
# PÁGINA 3: HISTÓRICO DE CÁLCULOS
# ============================================================================
elif page == "📈 Histórico de Cálculos":
    st.header("Histórico de Cálculos")
    st.markdown("Veja todos os cálculos de precificação que você já fez")
    st.markdown("---")
    
    if pricing_history:
        # Opções de filtro
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col2:
            show_favorites = st.checkbox("⭐ Apenas Favoritos", value=False)
        
        with col3:
            if st.button("🗑️ Limpar Histórico", use_container_width=True):
                save_pricing_history([])
                st.rerun()
        
        # Filtra histórico
        filtered_history = pricing_history
        if show_favorites:
            filtered_history = [calc for calc in pricing_history if calc.get("favorito", False)]
        
        if filtered_history:
            # Exibe histórico em ordem reversa (mais recente primeiro)
            for i, calc in enumerate(reversed(filtered_history)):
                original_index = len(pricing_history) - 1 - i
                
                # Header com estrela de favorito
                col_header1, col_header2 = st.columns([0.9, 0.1])
                
                with col_header1:
                    header_text = f"📅 {calc['data']} - {calc['servico']} ({calc['mes']})"
                    if calc.get("favorito", False):
                        header_text = f"⭐ {header_text}"
                
                with col_header2:
                    if st.button(
                        "⭐" if not calc.get("favorito", False) else "✅",
                        key=f"fav_{original_index}",
                        help="Adicionar aos favoritos" if not calc.get("favorito", False) else "Remover dos favoritos"
                    ):
                        pricing_history[original_index]["favorito"] = not pricing_history[original_index].get("favorito", False)
                        save_pricing_history(pricing_history)
                        st.rerun()
                
                with st.expander(header_text, expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**⚙️ Configuração**")
                        st.write(f"Preço Original: R$ {calc['preco_original']:.2f}")
                        st.write(f"Custo Serviço: R$ {calc['custo_servico']:.2f}")
                        st.write(f"Preço Promocional: R$ {calc['preco_promocional']:.2f}")
                        st.write(f"Comissão: {calc['comissao_percentual']:.1f}%")
                        st.write(f"Lucro Adicional: {calc['lucro_adicional']:.1f}%")
                    
                    with col2:
                        st.markdown("**📊 Sem Promoção**")
                        st.write(f"Demanda: {calc['demanda']} atendimentos")
                        st.write(f"Receita: R$ {calc['receita_sem_promo']:,.2f}")
                        st.write(f"Comissão: R$ {calc['comissao_sem_promo']:,.2f}")
                        st.write(f"Custo: R$ {calc['custo_sem_promo']:,.2f}")
                        st.write(f"**Lucro: R$ {calc['lucro_sem_promo']:,.2f}**")
                    
                    with col3:
                        st.markdown("**💰 Com Promoção**")
                        st.write(f"Quantidade: {calc['quantidade_necessaria']} atendimentos")
                        st.write(f"Receita: R$ {calc['receita_com_promo']:,.2f}")
                        st.write(f"Comissão: R$ {calc['comissao_com_promo']:,.2f}")
                        st.write(f"Custo: R$ {calc['custo_com_promo']:,.2f}")
                        st.write(f"**Lucro: R$ {calc['lucro_com_promo']:,.2f}**")
                    
                    # Botão para deletar
                    if st.button("🗑️ Deletar este cálculo", key=f"delete_{original_index}", use_container_width=True):
                        pricing_history.pop(original_index)
                        save_pricing_history(pricing_history)
                        st.rerun()
        else:
            st.info("📭 Nenhum cálculo favorito encontrado.")
    else:
        st.info("📭 Nenhum cálculo salvo ainda. Vá para 'Precificação Inteligente' e salve seus cálculos!")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888; font-size: 12px;'>"
    "Spa Dashboard © 2024 | Desenvolvido com Streamlit"
    "</p>",
    unsafe_allow_html=True
)
