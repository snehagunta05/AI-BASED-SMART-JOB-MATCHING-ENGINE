"""Main entry point for the Smart Job Matching Engine"""

from src.api.routes import create_app


def main():
    """Run the Flask API server"""
    app = create_app()
    print("=" * 60)
    print("AI-Based Smart Job Matching Engine")
    print("=" * 60)
    print("\nStarting API server...")
    print("API available at: http://localhost:5000")
    print("\nEndpoints:")
    print("  - GET  /api/health           - Health check")
    print("  - GET  /api/candidates      - List all candidates")
    print("  - GET  /api/jobs            - List all jobs")
    print("  - POST /api/match           - Match candidate to jobs")
    print("  - POST /api/match/candidates - Match candidates to job")
    print("  - GET  /api/match/all       - Get all matches")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    main()
