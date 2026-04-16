import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    categories = ['Speed', 'Power', 'Skill', 'Agility', 'Stamina']
    values = [3, 4, 5, 2, 4]

    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()

    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))

    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    st.pyplot(fig)

if __name__ == "__main__":    main()
