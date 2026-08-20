import api from '../services/api';

/**
 * analysisService — Handles communication with the unified FastAPI analysis endpoint.
 */
export const analysisService = {
  /**
   * Run the full end-to-end analysis pipeline.
   * @param {number} latitude 
   * @param {number} longitude 
   * @param {string} siteName 
   * @returns {Promise<Object>} The unified analysis JSON response
   */
  async runAnalysis(latitude, longitude, siteName) {
    // We pass latitude, longitude, and site_name matching the AnalysisRequest schema
    const { data } = await api.post('/analysis/', {
      latitude: parseFloat(latitude),
      longitude: parseFloat(longitude),
      site_name: siteName
    });
    return data;
  },

  /**
   * Fetch the user's saved site analyses history.
   * @returns {Promise<Array>} List of saved site analyses.
   */
  async getHistory() {
    const { data } = await api.get('/analysis/history');
    return data;
  },

  /**
   * Delete a saved site analysis from history.
   * @param {number} analysisId 
   * @returns {Promise<Object>}
   */
  async deleteHistory(analysisId) {
    const { data } = await api.delete(`/analysis/history/${analysisId}`);
    return data;
  }
};
