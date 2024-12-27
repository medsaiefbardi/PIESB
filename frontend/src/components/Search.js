import React, { useState } from "react";
import axios from "axios";

function Search() {
  const [competence, setCompetence] = useState(""); // Compétence entrée par l'utilisateur
  const [results, setResults] = useState({ programs: [], metiers: [] }); // Résultats de l'API
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!competence) return;
    setLoading(true);
    setError("");
    try {
      const response = await axios.get("http://localhost:5000/recommend", {
        params: { competence },
      });
      setResults(response.data);
    } catch (err) {
      setError("Erreur lors de la récupération des données.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Système de Recommandation</h1>
      <input
        type="text"
        placeholder="Entrez une compétence..."
        value={competence}
        onChange={(e) => setCompetence(e.target.value)}
      />
      <button onClick={handleSearch} disabled={loading}>
        {loading ? "Recherche en cours..." : "Rechercher"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Programmes Recommandés</h2>
      <ul>
        {results.programs.map((program, index) => (
          <li key={index}>{program.Compétences}</li>
        ))}
      </ul>

      <h2>Métiers Recommandés</h2>
      <ul>
        {results.metiers.map((metier, index) => (
          <li key={index}>{metier.Compétences}</li>
        ))}
      </ul>
    </div>
  );
}

export default Search;
