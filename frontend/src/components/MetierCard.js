import React from "react";
import styled from "styled-components";

const Card = styled.div`
    border: 1px solid #ddd;
    margin: 10px;
    padding: 10px;
    border-radius: 8px;
`;

function MetierCard({ metier }) {
    return (
        <Card>
            <h3>{metier.Domaine}</h3>
            <p>{metier.Competences.join(", ")}</p>
        </Card>
    );
}

export default MetierCard;
