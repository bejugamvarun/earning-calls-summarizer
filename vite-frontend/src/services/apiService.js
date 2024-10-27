const BASE_URL = 'http://localhost:8000';

class ApiService {
  async summarizeEarnings(companyName, year) {
    try {
      const response = await fetch(`${BASE_URL}/summarize/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ company_name: companyName, year: year }),
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch summary for ${companyName}: ${response.statusText}`);
      }

      const data = await response.json();
      return data.summary;
    } catch (error) {
      console.error('Error in summarizeEarnings:', error);
      throw error;
    }
  }

  async compareEarnings(companies, year) {
    try {
      const response = await fetch(`${BASE_URL}/compare/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ company_names: companies, year: year }),
      });

      if (!response.ok) {
        throw new Error(`Failed to compare earnings: ${response.statusText}`);
      }

      const data = await response.json();
      return data.comparative_report;
    } catch (error) {
      console.error('Error in compareEarnings:', error);
      throw error;
    }
  }
}

export default new ApiService();
