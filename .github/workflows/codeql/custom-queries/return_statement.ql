/**
 * @id codeql/custom-queries/return-statement
 * @name Return statements
 * @description Finds return statements that return 'null'.
 * @kind problem
 * @tags return
 *       statement
 *       null
 */

import csharp

from ReturnStmt r
where r.getExpr() instanceof NullLiteral
select r, "This return statement returns 'null' value."
