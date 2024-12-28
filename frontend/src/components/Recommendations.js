import React, { useState } from "react";
import styled from "styled-components";

const Container = styled.div`
    margin: 20px auto;
    width: 80%;
`;

const RecommendationCard = styled.div`
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    background-color: #f9f9f9;
`;

const Table = styled.div`
    display: table;
    width: 100%;
    border-collapse: collapse;
`;

const TableRow = styled.div`
    display: table-row;
    border-bottom: 1px solid #ddd;
`;

const TableCell = styled.div`
    display: table-cell;
    padding: 8px;
    vertical-align: top;
    font-size: 18px;
    text-align: left;

    &:first-child {
        background-color: #800000;
        color: #fff;
        font-weight: bold;
        width: 20%;
        text-align: center;
    }

    &:last-child {
        color: #555;
    }
`;

const Link = styled.a`
    display: block;
    margin-top: 10px;
    padding: 5px 10px;
    background-color: #007bff;
    color: white;
    border-radius: 3px;
    text-decoration: none;
    text-align: center;
    font-size: 18px;

    &:hover {
        background-color: rgb(179, 0, 0);
    }
`;

const Button = styled.button`
    background: none;
    border: none;
    color: rgb(0, 0, 0);
    cursor: pointer;
    font-size: 18px;
    padding: 0;
    margin-left: 5px;

    &:hover {
        text-decoration: underline;
    }
`;

function Recommendations({ recommendations }) {
    const [expanded, setExpanded] = useState({});

    const toggleExpand = (index) => {
        setExpanded((prev) => ({ ...prev, [index]: !prev[index] }));
    };
    function renderField(field) {
        return Array.isArray(field) && field.length > 0
            ? field.join(", ")
            : "Aucun disponible";
    }
    const renderContent = (content, index) => {
        if (Array.isArray(content)) {
            return (
                <ul style={{ margin: 0, paddingLeft: "20px", fontSize: "18px" }}>
                    {content.map((item, idx) => (
                        <li key={idx}>{item}</li>
                    ))}
                </ul>
            );
        }

        const isLongText = typeof content === "string" && content.length > 150;
        const isExpanded = expanded[index] || false;

        if (isLongText) {
            return (
                <span>
                    {isExpanded ? content : `${content.substring(0, 150)}...`}
                    <Button onClick={() => toggleExpand(index)}>
                        {isExpanded ? "Voir moins" : "Voir plus"}
                    </Button>
                </span>
            );
        }

        return <span>{content}</span>;
    };

    return (
        <Container>
            {recommendations.length > 0 ? (
                recommendations.map((rec, index) => (
                    <RecommendationCard key={index}>
                        <Table>
                            <TableRow>
                                <TableCell>Objectifs</TableCell>
                                <TableCell>{renderContent(rec.Objectifs, `${index}-objectifs`)}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Compétences</TableCell>
                                <TableCell>
                                    {renderContent(rec.Competences, `${index}-Competences`)}
                                </TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Contenu</TableCell>
                                <TableCell>{renderContent(rec.Contenu, `${index}-contenu`)}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Métiers</TableCell>
                                <TableCell>
                                {renderContent(rec.Métiers, `${index}-Métiers`)}
                                </TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Secteurs d'activité</TableCell>
                                <TableCell>
                                {renderContent(rec["Secteurs d’activité"])}
                                </TableCell>
                            </TableRow>
                        </Table>
                        <Link href={rec.URL} target="_blank" rel="noopener noreferrer">
                            Voir le programme
                        </Link>
                    </RecommendationCard>
                ))
            ) : (
                <p style={{ fontSize: "18px" }}>Aucune recommandation trouvée</p>
            )}
        </Container>
    );
}

export default Recommendations;
