import React, { useState } from "react";
import styled from "styled-components";
import CompetenceInput from "./components/CompetenceInput";
import Recommendations from "./components/Recommendations";
import { fetchRecommendations } from "./services/api";

const AppContainer = styled.div`
    text-align: center;
    padding: 20px;
    font-family: "Playfair Display", serif; /* Police élégante */
`;

const Header = styled.div`
    display: flex;
    align-items: center;
    margin-bottom: 20px;
`;

const LogoContainer = styled.div`
    background-color: white; /* Fond blanc pour le logo */
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
`;

const Logo = styled.img`
    width: 240px; /* Taille doublée */
    height: auto;
`;

const TitleContainer = styled.div`
    flex-grow: 1;
    background-color: #800020; /* Rouge bordeaux */
    text-align: center;
    padding: 10px;
`;

const Title = styled.h1`
    font-size: 36px;
    color: white; /* Texte blanc */
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 0;
`;

const ErrorMessage = styled.p`
    color: red;
    font-weight: bold;
`;

function App() {
    const [recommendations, setRecommendations] = useState([]);
    const [error, setError] = useState(null);

    const handleSearch = async (competence) => {
        try {
            const { programs } = await fetchRecommendations(competence);

            

            setRecommendations(programs);
            setError(null);
        } catch (err) {
            setError("Erreur lors de la récupération des recommandations.");
            console.error(err);
        }
    };

    return (
        <AppContainer>
            <Header>
                <LogoContainer>
                    <Logo
                        src="https://www.esb.tn/wp-content/uploads/2019/04/logo_esb_sticky.svg"
                        alt="ESB Logo"
                    />
                </LogoContainer>
                <TitleContainer>
                    <Title>Recherchez une compétence</Title>
                </TitleContainer>
            </Header>
            <CompetenceInput onSubmit={handleSearch} />
            {error && <ErrorMessage>{error}</ErrorMessage>}
            <Recommendations recommendations={recommendations} />
        </AppContainer>
    );
}

export default App;
