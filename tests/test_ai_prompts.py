from shoshin import ai


def test_ai_query(document_store_mock, mocker):
    # Ensure ai.query returns a text response
    ds = document_store_mock
    pipeline = mocker.patch("shoshin.ai.GenerativeQAPipeline")()
    pipeline.run.return_value = {"results": "Test response"}
    # Test
    response = ai.query(ds.retriever, "Test question")
    # Check
    assert response == "Test response"
    assert pipeline.run.call_count == 1
    pipeline.run.assert_called_with(params={"Retriever": {"top_k": 10}}, query="Test question")
