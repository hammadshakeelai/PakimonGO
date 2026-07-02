with open('docs/api/OPENAPI_DRAFT.yaml', 'r') as f:
    lines = f.readlines()

first_idx = 185
first_end = 209
second_idx = 361
second_end = 415

new_submissions = [
    '  /submissions:\n',
    '    post:\n',
    '      summary: Submit a capture for scoring\n',
    '      operationId: createSubmission\n',
    '      x-status: implemented\n',
    '      x-requirements:\n',
    '        - FR-CAP-005\n',
    '        - FR-SCORE-003\n',
    '        - FR-SCORE-008\n',
    '      requestBody:\n',
    '        required: true\n',
    '        content:\n',
    '          application/json:\n',
    '            schema:\n',
    '              $ref: "#/components/schemas/CreateSubmissionRequest"\n',
    '      responses:\n',
    '        "200":\n',
    '          description: Submission created with precheck result\n',
    '          content:\n',
    '            application/json:\n',
    '              schema:\n',
    '                $ref: "#/components/schemas/Submission"\n',
    '        "400":\n',
    '          $ref: "#/components/responses/ValidationError"\n',
    '    get:\n',
    '      summary: List user submissions\n',
    '      operationId: listSubmissions\n',
    '      x-status: implemented\n',
    '      x-requirements:\n',
    '        - FR-CAP-005\n',
    '      parameters:\n',
    '        - name: limit\n',
    '          in: query\n',
    '          schema:\n',
    '            type: integer\n',
    '            default: 20\n',
    '            minimum: 1\n',
    '            maximum: 100\n',
    '        - name: offset\n',
    '          in: query\n',
    '          schema:\n',
    '            type: integer\n',
    '            default: 0\n',
    '            minimum: 0\n',
    '        - name: status\n',
    '          in: query\n',
    '          schema:\n',
    '            type: string\n',
    '            enum: [pending, prechecked, ai_evaluated, scored, capped, review, rejected, rolled_back]\n',
    '        - name: sort_by\n',
    '          in: query\n',
    '          schema:\n',
    '            type: string\n',
    '            enum: [createdAt, submittedAt, status, points, species]\n',
    '            default: createdAt\n',
    '        - name: sort_order\n',
    '          in: query\n',
    '          schema:\n',
    '            type: string\n',
    '            enum: [asc, desc]\n',
    '            default: desc\n',
    '        - name: include_sensitive\n',
    '          in: query\n',
    '          schema:\n',
    '            type: boolean\n',
    '            default: false\n',
    '          description: Include sensitive species (requires elevated permissions)\n',
    '      responses:\n',
    '        "200":\n',
    '          description: Paginated list of submissions\n',
    '          content:\n',
    '            application/json:\n',
    '              schema:\n',
    '                $ref: "#/components/schemas/PaginatedSubmissionListResponse"\n',
    '\n'
]

result = lines[:first_idx] + new_submissions + lines[first_end:second_idx] + lines[second_end:]

with open('docs/api/OPENAPI_DRAFT.yaml', 'w') as f:
    f.write(''.join(result))

print('File written successfully')