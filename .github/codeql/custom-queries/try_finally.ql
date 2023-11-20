/**
 * @id csharp/custom-queries/try-finally
 * @name Try-finally statements
 * @description Finds try-finally statements without a catch clause.
 * @kind problem
 * @tags try
 *       finally
 *       catch
 *       exceptions
 */

import csharp

from TryStmt t
where
  exists(t.getFinally()) and
  not exists(t.getACatchClause())
select t, "This try-finally block does not have a catch clause."
