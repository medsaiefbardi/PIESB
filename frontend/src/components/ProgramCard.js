import React from "react";
import styled from "styled-components";

const Card = styled.div`
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    margin: 10px;
    background-color: #f9f9f9;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h3`
    font-size: 20px;
    color: #444;
`;

const Competences = styled.p`
    font-size: 18px;
    color: #666;
`;

function ProgramCard({ program }) {
    return (
        <Card>
            <Title>{program.Module}</Title>
            <Competences>{program.Competences.join(", ")}</Competences>
        </Card>
    );
}

export default ProgramCard;
