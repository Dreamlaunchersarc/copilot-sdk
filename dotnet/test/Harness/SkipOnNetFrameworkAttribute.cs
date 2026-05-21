/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *--------------------------------------------------------------------------------------------*/

using System.Runtime.InteropServices;
using Xunit;

namespace GitHub.Copilot.SDK.Test.Harness;

/// <summary>
/// Skips the test when running on .NET Framework (e.g. net472).
/// </summary>
internal sealed class SkipOnNetFrameworkAttribute : FactAttribute
{
    public SkipOnNetFrameworkAttribute(string reason = "Not supported on .NET Framework")
    {
        if (RuntimeInformation.FrameworkDescription.StartsWith(".NET Framework", StringComparison.OrdinalIgnoreCase))
        {
            Skip = reason;
        }
    }
}
