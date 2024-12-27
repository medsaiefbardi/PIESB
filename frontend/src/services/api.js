const BASE_URL = "http://127.0.0.1:5000";

export async function fetchRecommendations(competence) {
    const response = await fetch(`${BASE_URL}/competences/recommend?competence=${competence}`);
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
}
export async function fetchSuggestions(query) {
    const response = await fetch(`http://127.0.0.1:5000/suggestions?query=${query}`);
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
}
