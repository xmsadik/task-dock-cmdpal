using System;
using ClaudeTasks.Services;
using Microsoft.CommandPalette.Extensions;
using Microsoft.CommandPalette.Extensions.Toolkit;

namespace ClaudeTasks;

public partial class ClaudeTasksCommandsProvider : CommandProvider
{
    private readonly ICommandItem[] _commands;
    private readonly ICommandItem _dockBand;
    private readonly SettingsManager _settingsManager = new();
    private readonly TaskStore _store;
    private readonly ProjectsPage _projectsPage;
    private readonly TasksSummaryPage _summaryPage;
    private readonly TasksBand _band;

    public ClaudeTasksCommandsProvider()
    {
        DisplayName = "Task Dock";
        Id = "TaskDock";
        Icon = IconHelpers.FromRelativePath("Assets\\StoreLogo.png");

        _store = new TaskStore(_settingsManager);
        _projectsPage = new ProjectsPage(_store, _settingsManager);
        _summaryPage = new TasksSummaryPage(_store, _settingsManager, _projectsPage);

        _commands = [
            new CommandItem(_projectsPage)
            {
                Title = DisplayName,
                Subtitle = "Browse local Claude projects and tasks",
                MoreCommands = [new CommandContextItem(_settingsManager.Settings.SettingsPage)],
            },
        ];

        _band = new TasksBand(_store, _summaryPage);

        // Command.Id must be non-empty or the host silently drops the band.
        _dockBand = new WrappedDockItem([_band], "TaskDock.dock.tasks", "Task Dock");

        Settings = _settingsManager.Settings;
    }

    public override ICommandItem[] TopLevelCommands() => _commands;

    public override ICommandItem[]? GetDockBands() => [_dockBand];

    public override void Dispose()
    {
        _band.Dispose();
        _summaryPage.Dispose();
        _projectsPage.Dispose();
        _store.Dispose();
        base.Dispose();
        GC.SuppressFinalize(this);
    }
}
