/**
 * @id codeql/custom-queries/empty-block
 * @name Empty blocks
 * @description Find empty block statements
 * @kind problem
 * @tags empty
 *       block
 *       statement
 */

import csharp

from BlockStmt blk
where blk.isEmpty()
select blk, "This is an empty block."
