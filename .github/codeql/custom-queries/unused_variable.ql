/**
 * @id csharp/custom-queries/unused-variable
 * @name Unused variable
 * @description Finds variables that are not accessed.
 * @kind problem
 * @tags variable
 *       access
 */

import csharp

from Variable v
where not exists(v.getAnAccess())
select v, "This variable is not accessed anywhere."
