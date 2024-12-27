import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { fetchSuggestions } from "../services/api";

const InputWrapper = styled.div`
    position: relative;
    width: 100%;
`;

const Input = styled.input`
    width: 100%;
    padding: 10px;
    font-size: 16px;
`;

const SuggestionsList = styled.ul`
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background: white;
    border: 1px solid #ddd;
    max-height: 200px;
    overflow-y: auto;
    z-index: 10;
    list-style: none;
    padding: 0;
    margin: 0;
`;

const SuggestionItem = styled.li`
    padding: 10px;
    font-size: 18px;
    text-align: left;
    cursor: pointer;

    &:hover {
        background: #f0f0f0;
    }
`;

const SubmitButton = styled.button`
    margin-top: 10px;
    padding: 10px 20px;
    font-size: 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
        background-color: #0056b3;
    }
`;

function CompetenceInput({ onSubmit }) {
    const [competence, setCompetence] = useState("");
    const [suggestions, setSuggestions] = useState([]);

    useEffect(() => {
        if (competence.length >= 3) {
            fetchSuggestions(competence).then(setSuggestions).catch(console.error);
        } else {
            setSuggestions([]);
        }
    }, [competence]);

    const handleSelect = (suggestion) => {
        setCompetence(""); // Vider la barre de recherche
        setSuggestions([]); // Effacer les suggestions
        onSubmit(suggestion); // Appeler la recherche avec la suggestion
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(competence);
        setCompetence(""); // Vider la barre de recherche
        setSuggestions([]); // Effacer les suggestions
    };

    return (
        <form onSubmit={handleSubmit}>
            <InputWrapper>
                <Input
                    type="text"
                    placeholder="Recherchez une compétence"
                    value={competence}
                    onChange={(e) => setCompetence(e.target.value)}
                />
                {suggestions.length > 0 && (
                    <SuggestionsList>
                        {suggestions.map((sug, index) => (
                            <SuggestionItem key={index} onClick={() => handleSelect(sug)}>
                                {sug}
                            </SuggestionItem>
                        ))}
                    </SuggestionsList>
                )}
            </InputWrapper>
            <SubmitButton type="submit">Rechercher</SubmitButton>
        </form>
    );
}

export default CompetenceInput;
