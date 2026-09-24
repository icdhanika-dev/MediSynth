from graph.neo4j_connection import driver
from config import NEO4J_DATABASE


def build_evidence_graph(case_id: str, analyses: list):

    with driver.session(database=NEO4J_DATABASE) as session:

        session.run(
            """
            MERGE (c:Case {id: $case_id})
            """,
            case_id=case_id
        )

        for analysis in analyses:

            session.run(
                """
                MATCH (c:Case {id: $case_id})

                MERGE (a:Agent {name: $agent_name})

                MERGE (c)-[:ANALYZED_BY]->(a)
                """,
                case_id=case_id,
                agent_name=analysis.agent
            )

            for finding in analysis.findings:

                result = session.run(
                    """
                    MATCH (a:Agent {name: $agent_name})

                    CREATE (f:Finding {
                        text: $finding,
                        confidence: $confidence
                    })

                    CREATE (a)-[:OBSERVED]->(f)

                    RETURN elementId(f) AS finding_id
                    """,
                    agent_name=analysis.agent,
                    finding=finding.finding,
                    confidence=finding.confidence
                )

                finding_id = result.single()["finding_id"]

                session.run(
                    """
                    MATCH (f:Finding)
                    WHERE elementId(f) = $finding_id

                    CREATE (e:Evidence {
                        text: $evidence
                    })

                    CREATE (f)-[:SUPPORTED_BY]->(e)
                    """,
                    finding_id=finding_id,
                    evidence=finding.evidence
                )

            for condition in analysis.possible_conditions:

                session.run(
                    """
                    MATCH (a:Agent {name: $agent_name})

                    MERGE (c:Condition {name: $condition})

                    CREATE (a)-[:PROPOSES]->(c)
                    """,
                    agent_name=analysis.agent,
                    condition=condition
                )

    print("Evidence graph created.")